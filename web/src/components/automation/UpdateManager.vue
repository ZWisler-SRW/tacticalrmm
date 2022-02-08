<template>
  <q-card>
    <q-bar v-if="modal">
      <q-btn @click="getWindowsUpdates" class="q-mr-sm" dense flat push icon="refresh" />Update Manager
      <q-space />
      <q-btn dense flat icon="close" v-close-popup>
        <q-tooltip content-class="bg-white text-primary">Close</q-tooltip>
      </q-btn>
    </q-bar>
    <q-table
      :table-class="{ 'table-bgcolor': !$q.dark.isActive, 'table-bgcolor-dark': $q.dark.isActive }"
      class="tabs-tbl-sticky"
      :style="{ 'max-height': tabHeight ? tabHeight : `${$q.screen.height - 33}px` }"
      :rows="windowsUpdates"
      :columns="columns"
      :title="modal ? 'Windows Updates' : ''"
      :pagination="{ sortBy: 'status', descending: true, rowsPerPage: 0 }"
      :loading="loading"
      :filter="filter"
      virtual-scroll
      dense
      binary-state-sort
      :rows-per-page-options="[0]"
    >
      <template v-slot:top>
        <!--<q-btn class="q-pr-sm" dense flat push @click="getWindowsUpdates" icon="refresh" />-->
        <q-space />
        <q-input v-model="filter" outlined label="Search" dense clearable class="q-pr-sm">
          <template v-slot:prepend>
            <q-icon name="search" color="primary" />
          </template>
        </q-input>
        <export-table-btn :data="windowsUpdates" :columns="columns" />
      </template>

      <template v-slot:top-row>
        <q-tr v-if="Array.isArray(windowsUpdates) && windowsUpdates.length === 1000">
          <q-td colspan="100%">
            <q-icon name="warning" color="warning" />
            Results are limited to 1000 rows.
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </q-card>
</template>

<script>
// composition api
import { ref, onMounted } from "vue";
import { fetchWindowsUpdates } from "@/api/winupdates";

// ui components
import ExportTableBtn from "@/components/ui/ExportTableBtn.vue";

const columns = [
  {
    name: "status",
    label: "Status",
    field: "status",
    align: "left",
    sortable: true,
  },
  {
    name: "severity",
    label: "Severity",
    field: "severity",
    align: "left",
    sortable: true,
  },
  {
    name: "kb",
    label: "KB",
    field: "kb",
    align: "left",
    sortable: true,
  },
  {
    name: "name",
    label: "Name",
    field: "name",
    align: "left",
    sortable: true,
  },
  {
    name: "agents_pending",
    label: "Agent Pending Install Count",
    field: "agents_pending",
    align: "left",
    sortable: true,
  },
  {
    name: "agents_installed",
    label: "Agent Installed Count",
    field: "agents_installed",
    align: "left",
    sortable: true,
  },
];

export default {
  name: "UpdateModal",
  components: {
    ExportTableBtn,
  },
  props: {
    tabHeight: String,
    modal: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    // set main debug log functionality
    const windowsUpdates = ref([]);

    const loading = ref(false);
    const filter = ref("");

    async function getWindowsUpdates() {
      loading.value = true;
      try {
        windowsUpdates.value = await fetchWindowsUpdates();
      } catch (e) {
        console.error(e);
      }
      loading.value = false;
    }

    // vue component hooks
    onMounted(() => {
      getWindowsUpdates();
    });

    return {
      // data
      windowsUpdates,
      loading,
      filter,

      // non-reactive data
      columns,

      // methods
      getWindowsUpdates,
    };
  },
};
</script>