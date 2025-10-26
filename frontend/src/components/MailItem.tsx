import type { Mail } from "../api/types";

export function MailItem({ mail }: { mail: Mail }) {
  const formattedDate = new Date(mail.received_at).toLocaleString();

  return (
    <li className="p-4 hover:bg-gray-50 transition-colors border-b border-gray-200">
      <p className="font-semibold text-gray-800 text-base mb-1">
        {mail.subject}
      </p>

      <div className="flex justify-between text-sm mb-2 text-gray-600">
        <span>Od: {mail.sender}</span>
        <span>{formattedDate}</span>
      </div>

      <p className="text-sm text-gray-700 text-justify leading-relaxed">
        {mail.attachment_summary}
      </p>
    </li>
  );
}
