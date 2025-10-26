import type { Mail } from "../api/types";
import { MailItem } from "./MailItem";

export function MailList({ mails }: { mails: Mail[] }) {
  if (mails.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        Brak wiadomości do wyświetlenia.
      </div>
    );
  }

  return (
    <ul className="divide-y divide-gray-200">
      {mails.map((mail) => (
        <MailItem key={mail.id} mail={mail} />
      ))}
    </ul>
  );
}
