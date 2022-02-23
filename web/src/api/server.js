import axios from "axios"

const baseUrl = "/core"

export async function fetchServerInfo(params = {}) {
    try {
        const { data } = await axios.get(`${baseUrl}/serverinfo/`, { params: params })
        return data
    } catch (e) { console.error(e) }
}