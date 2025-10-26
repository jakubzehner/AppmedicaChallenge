import { useEffect, useState, useRef } from "react";
import { mailApi } from "../api/client";
import { MailList } from "./MailList";
import { PaginationControls } from "./PaginationControls";
import type { Mail } from "../api/types";

export function MailBoard() {
  const [mails, setMails] = useState<Mail[]>([]);
  const [skip, setSkip] = useState(0);
  const limit = 8;
  const [loading, setLoading] = useState(false);
  const [isLastPage, setIsLastPage] = useState(false);
  const wasLastPage = useRef(false);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const data = await mailApi.getAll(skip, limit);

        //NOTE: this is a consequence of using very simple pagination with no total count
        //back to previous page if no data
        if (data.length === 0 && skip > 0) {
          setSkip((prev) => Math.max(0, prev - limit));
          wasLastPage.current = true;
          return;
        }

        setMails(data);
        setIsLastPage(wasLastPage.current || data.length < limit);
        wasLastPage.current = false;
      } catch (err) {
        console.error("Failed to fetch mails:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, [skip]);

  const handleNext = () => {
    if (!isLastPage) setSkip((prev) => prev + limit);
  };

  const handlePrev = () => {
    if (skip > 0) setSkip((prev) => Math.max(0, prev - limit));
  };

  return (
    <div className="max-w-5xl mx-auto mt-8 p-4 bg-white shadow-md rounded-2xl flex flex-col h-[95vh]">
      <h1 className="text-2xl font-semibold mb-4 text-gray-800">
        📧 Skrzynka odbiorcza
      </h1>

      <div className="flex-1 overflow-y-auto border border-gray-200 rounded-xl">
        {loading ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            Ładowanie...
          </div>
        ) : (
          <MailList mails={mails} />
        )}
      </div>

      <div className="mt-4">
        <PaginationControls
          onPrev={handlePrev}
          onNext={handleNext}
          disablePrev={skip === 0}
          disableNext={isLastPage || mails.length === 0}
        />
      </div>
    </div>
  );
}
