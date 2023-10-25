import { get, post } from "@/services/ajax";


export function getConfig() {
  return get("static/config.json", null, { baseURL: "./" });
}


