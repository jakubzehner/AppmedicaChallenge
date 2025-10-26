import { MailListSchema } from "./schemas";
import type { Mail } from "./types";

export const API_URL = "http://localhost:8000/api";

export const mailApi = {
  async getAll(skip: number = 0, limit: number = 8): Promise<Mail[]> {
    const response = await fetch(`${API_URL}/mail?skip=${skip}&limit=${limit}`);
    return MailListSchema.parse(await response.json());
  },
};
