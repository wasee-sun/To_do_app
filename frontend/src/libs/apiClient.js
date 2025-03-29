const HTTPS = process.env.HTTPS == "true";

export class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async request(endpoint, method, data = null, isMultipart = null) {
    const url = `${this.baseURL}${endpoint}`;
    const options = {
      method: method,
      headers: {
        Accept: "application/json",
        "NEXT-X-API-KEY": process.env.NEXT_PUBLIC_API_SECRET_KEY,
        ...(HTTPS && { Referer: process.env.NEXT_PUBLIC_BASE_HTTPS_URL }),
      },
      credentials: "include",
    };

    if (isMultipart && data instanceof FormData) {
      // For multipart/form-data
      delete options.headers["Content-Type"];
      options.body = data;
    } else if (data) {
      // For application/json
      options.headers["Content-Type"] = "application/json";
      options.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url, options);

      if (response.status >= 400) {
        const error = await response.json();
        console.log(error);
        return null;
      }

      if (response.status == 204) {
        return null;
      }
      const responseData = await response.json();
      return responseData;
    } catch (error) {
      console.error("Fetch error:", error);
      throw error;
    }
  }

  async get(endpoint) {
    return await this.request(endpoint, "GET", null);
  }

  async post(endpoint, data) {
    return await this.request(endpoint, "POST", data);
  }

  async patch(endpoint, data, isMultipart = false) {
    return await this.request(endpoint, "PATCH", data, isMultipart);
  }

  async put(endpoint, data) {
    return await this.request(endpoint, "PUT", data);
  }

  async delete(endpoint, data = null) {
    return await this.request(endpoint, "DELETE", data);
  }
}
