import axios from "axios"

const baseUrl = "/winupdate"

// win updates api functions
export async function fetchAgentUpdates(agent_id, params = {}) {
  try {
    const { data } = await axios.get(`${baseUrl}/${agent_id}/`, { params: params })
    return data
  } catch (e) { console.error(e) }
}

export async function runAgentUpdateScan(agent_id) {
  const { data } = await axios.post(`${baseUrl}/${agent_id}/scan/`)
  return data
}

export async function runAgentUpdateInstall(agent_id) {
  const { data } = await axios.post(`${baseUrl}/${agent_id}/install/`)
  return data
}

export async function editAgentUpdate(id, payload) {
  const { data } = await axios.put(`${baseUrl}/${id}/`, payload)
  return data
}

/*
  Begin update manager calls
*/

export async function fetchWindowsUpdates(params = {}) {
  try {
    const { data } = await axios.get(`${baseUrl}/retrieve`, { params: params })
    return data
  } catch (e) { console.error(e) }
}

export async function populateWindowsUpdates() {
  try {
    const { data } = await axios.patch(`${baseUrl}/populate/`)
    return data
  } catch (e) { console.error(e) }
}

export async function updateAllWindowsUpdates(kb, payload) {
  try {
    const { data } = await axios.put(`${baseUrl}/all/${kb}/`, payload)
    return data
  } catch (e) { console.error(e) }
}