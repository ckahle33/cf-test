import { parse } from "cookie";

export default {
  async fetch(request) {
    const docs_url = new URL("https://developers.cloudflare.com/workers/learning")
    const statusCode = 301;

    let url = new URL(request.url);
    console.log(request.url)
    let user_agent = request.headers.get('user-agent')
    console.log(user_agent)
    const cookie = parse(request.headers.get("Cookie") || "");    
    if (cookie && cookie['cf-noredir'] == 'true') {
      return fetch(request)
    } else if (user_agent.includes('curl') == true) {
      url = docs_url      
      return Response.redirect(url, statusCode);
    }

    return fetch(request) 
    
  },
};