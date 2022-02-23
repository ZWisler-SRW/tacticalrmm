import { ref, onMounted } from "vue"
import { fetchGroups } from "@/api/groups"
import { formatGroupOptions } from "@/utils/format"

// group dropdown
export function useGroupDropdown(onMount = false) {
    const group = ref(null)
    const groups = ref([])
    const groupOptions = ref([])

    // specifing flat returns an array of hostnames versus {value:id, label: hostname}
    async function getGroupOptions(flat = false) {
        groupOptions.value = formatGroupOptions(await fetchGroups(), flat)
    }

    if (onMount) onMounted(getGroupOptions)

    return {
        //data
        group,
        groups,
        groupOptions,

        //methods
        getGroupOptions
    }
}
