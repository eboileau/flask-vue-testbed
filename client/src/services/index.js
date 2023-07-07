import axios from 'axios'

const HTTP = axios.create({
  baseURL: `http://127.0.0.1:5000`,
  withCredentials: true,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})

export default {
  getConcurrent(endpoints) {
    return Promise.all(endpoints.map((endpoint) => HTTP.get(endpoint)))
  },
  getEndpoint(endpoint) {
    return HTTP.get(endpoint)
  },
  postEndpoint(endpoint, payload) {
    return HTTP.post(endpoint, payload)
  },
}
