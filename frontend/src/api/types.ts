export type Mail = {
  id: number;
  subject: string;
  sender: string;
  received_at: string; // ISO date string
  attachment_summary: string;
};
