import axios from "axios"
import { URL } from "constants/API"
import isRetryAllowed from "is-retry-allowed"
import { getLocalStorage } from "utils/token"


const RETRIES = 3

const API = axios.create({
  withCredentials: false,
  headers: {
    "Content-type": "application/json",
    // "X-Requested-With": "XMLHttpRequest",
    // 'Access-Control-Allow-Origin' : '*',
  },
})

const switchService = (configUrl) => {
  let prefix = configUrl.split("/")[0];
  
  if (prefix === URL['ENTRYPOINT'].prefix) {
    return URL['ENTRYPOINT'].value
  } else if (prefix === URL['META'].prefix) {
    return URL['META'].value
  }
  return window.location.host;
}

API.interceptors.request.use(
  (config) => {
    if (!config?.headers?.Authorization)
      config.headers = {
        ...config.headers,
        Authorization: getLocalStorage("au") ? `Bearer ${getLocalStorage("au")}` : null,
      }
    config.retryCount = config.retryCount || 0
    if (config.url === "http://172.16.16.147:8003/image") {
      config.baseURL = URL.META.value
    } else {
      config.baseURL = switchService(config.url)
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

API.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response.status === 401 && window.location.pathname !== "/") {
      const hostOrigin = window.location.origin
      window.location.href = hostOrigin
    }
    let config = error.config,
      shouldRetry =
        error.code !== "ECONNABORTED" &&
        error.response &&
        error.response.status === 429 &&
        config.retryCount < RETRIES &&
        isRetryAllowed(error)

    if (shouldRetry) {
      config.retryCount += 1
      let delay = error.response.headers["retry-after"] || 30
      return new Promise((resolve) =>
        setTimeout(() => resolve(axios(config)), delay * 1e3),
      )
    } else if (
      ["ECONNREFUSED", "ETIMEDOUT", "ECONNRESET"].includes(error.code) &&
      config.retryCount < RETRIES
    ) {
      config.retryCount += 1
      return new Promise((resolve) => setTimeout(() => resolve(axios(config)), 8e3))
    }
    return Promise.reject(error)
  },
)

export default API
