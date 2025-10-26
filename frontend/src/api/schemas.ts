import z from "zod";

export const MailSchema = z.object({
  id: z.int(),
  subject: z.string(),
  sender: z.string(),
  received_at: z.iso.datetime({ local: true }),
  attachment_summary: z.string(),
});

export const MailListSchema = z.array(MailSchema);
