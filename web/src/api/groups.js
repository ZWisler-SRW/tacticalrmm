import axios from "axios"

const baseUrl = "/groups"

export async function fetchGroups() {
    try {
        const { data } = await axios.get(`${baseUrl}/`)
        return data
    } catch (e) { console.error(e) }
}

export async function saveGroup(payload) {
    try {
        const { data } = await axios.post(`${baseUrl}/create/`, payload)
        return data
    } catch (e) { console.error(e) }
}

export async function editGroup(id, payload) {
    try {
        const { data } = await axios.put(`${baseUrl}/edit/${id}/`, payload)
        return data
    } catch (e) { console.error(e) }
}

export async function deleteGroup(id, payload) {
    try {
        const { data } = await axios.delete(`${baseUrl}/delete/${id}/`, payload)
        return data
    } catch (e) { console.error(e) }
}

export async function addGroupMember(id, payload) {
    try {
        const { data } = await axios.put(`${baseUrl}/add/${id}/`, payload)
        return data
    } catch (e) { console.error(e) }
}

export async function removeGroupMember(id, payload) {
    try {
        const { data } = await axios.put(`${baseUrl}/remove/${id}/`, payload)
        return data
    } catch (e) { console.error(e) }
}