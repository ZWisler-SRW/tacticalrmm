<template>
  <q-card>
    <q-bar v-if="modal">
      <!--<q-btn @click="getWindowsUpdates" class="q-mr-sm" dense flat push icon="refresh" />-->Update Manager
      <q-space />
      <q-btn dense flat icon="close" v-close-popup>
        <q-tooltip content-class="bg-white text-primary">Close</q-tooltip>
      </q-btn>
    </q-bar>

    <q-table
      dense
      :table-class="{ 'table-bgcolor': !$q.dark.isActive, 'table-bgcolor-dark': $q.dark.isActive }"
      class="tabs-tbl-sticky"
      :style="{ 'max-height': tabHeight }"
      :rows="windowsUpdates"
      :columns="columns"
      :filter="filter"
      binary-state-sort
      :pagination="pagination"
      :rows-per-page-options="[25, 50, 100]"
      virtual-scroll
      :loading="loading"
      no-data-label="No Windows Updates"
    >
      <template v-slot:top>
        <q-btn
          label="Refresh Updates"
          dense
          flat
          push
          no-caps
          @click="updateWindowsUpdates"
          icon="refresh"
          class="q-mr-sm"
        />
        <q-space />

        <q-input v-model="filter" outlined label="Search" dense clearable class="q-pr-sm">
          <template v-slot:prepend>
            <q-icon name="search" color="primary" />
          </template>
        </q-input>
        <export-table-btn :data="windowsUpdates" :columns="columns" />
      </template>

      <template v-slot:loading>
        <q-inner-loading showing color="primary" />
      </template>

      <template v-slot:body="props">
        <q-tr :props="props">
          <q-menu context-menu>
            <q-list dense style="min-width: 100px">
              <q-item clickable v-close-popup @click="editWindowsUpdate(props.row.kb, 'inherit')">
                <q-item-section>Inherit</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="editWindowsUpdate(props.row.kb, 'approve')">
                <q-item-section>Approve</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="editWindowsUpdate(props.row.kb, 'ignore')">
                <q-item-section>Ignore</q-item-section>
              </q-item>
              <q-item clickable v-close-popup @click="editWindowsUpdate(props.row.kb, 'nothing')">
                <q-item-section>Do Nothing</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
          <!-- policy -->
          <q-td>
            <span v-if="props.row.status === 'nothing'" name="fiber_manual_record" color="grey"> Do Nothing </span>
            <span v-else-if="props.row.status === 'approve'" name="fas fa-check" color="primary"> Approve </span>
            <span v-else-if="props.row.status === 'ignore'" name="fas fa-check" color="negative"> Ignore </span>
            <span v-else-if="props.row.status === 'inherit'" name="fiber_manual_record" color="accent"> Inherit</span>
            <span v-else-if="props.row.status === 'default'" name="fiber_manual_record" color="grey"> Default</span>
          </q-td>
          <q-td>{{ !props.row.severity ? "Not Defined" : props.row.severity }}</q-td>
          <q-td>{{ props.row.kb }}</q-td>
          <!--<q-td>{{ truncateText(props.row.name, 75) }}</q-td>-->
          <q-td @click="showUpdateDetails(props.row.update_data)">
            <span style="cursor: pointer; text-decoration: underline" class="text-primary">{{
              truncateText(props.row.name, 75)
            }}</span>
          </q-td>
          <q-td @click="showAgentsPendingList(props.row.update_data)">
            <span style="cursor: pointer; text-decoration: underline" class="text-primary">{{
              props.row.update_data.pending_agents.length
            }}</span>
          </q-td>
          <q-td @click="showAgentsInstalledList(props.row.update_data)">
            <span style="cursor: pointer; text-decoration: underline" class="text-primary">{{
              props.row.update_data.installed_agents.length
            }}</span>
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </q-card>
</template>

<script>
// composition api
import { ref, onMounted } from "vue";
import { useQuasar } from "quasar";
import { fetchWindowsUpdates, populateWindowsUpdates, updateAllWindowsUpdates } from "@/api/winupdates";
import { notifySuccess } from "@/utils/notify";
import { truncateText } from "@/utils/format";

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
    sortable: false,
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
  name: "WindowsUpdateManager",
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
    const windowsUpdates = ref([]);

    const filter = ref("");
    const pagination = ref({
      sortBy: "kb",
      descending: true,
      rowsPerPage: 25,
    });
    const loading = ref(false);

    const $q = useQuasar();

    async function getWindowsUpdates() {
      loading.value = true;
      try {
        windowsUpdates.value = await fetchWindowsUpdates();
        notifySuccess("Fetched and updated Windows Updates");
      } catch (e) {
        console.error(e);
      }
      loading.value = false;
    }

    async function updateWindowsUpdates() {
      loading.value = true;
      try {
        populateWindowsUpdates().then(() => {
          getWindowsUpdates();
        });
      } catch (e) {
        console.error(e);
      }
      loading.value = false;
    }

    async function editWindowsUpdate(kb, action) {
      loading.value = true;
      try {
        const result = await updateAllWindowsUpdates(kb, { action: action });
        notifySuccess(result);
        getWindowsUpdates();
      } catch (e) {
        console.error(e);
      }
      loading.value = false;
    }

    function showUpdateDetails(update) {
      let support_urls = "";
      update.more_info_urls.forEach(u => {
        support_urls += `<a href='${u}' target='_blank'>${u}</a><br/>`;
      });
      let cats = update.categories.join(", ");
      $q.dialog({
        title: update.title,
        message:
          `<b>Categories:</b> ${cats}<br/><br/>` +
          "<b>Description</b><br/>" +
          update.description.split(". ").join(".<br />") +
          `<br/><br/><b>Support Urls</b><br/>${support_urls}`,
        html: true,
        fullWidth: true,
      });
    }

    function showAgentsPendingList(update) {
      $q.dialog({
        title: "Agents Pending The Update",
        message: update.pending_agents.length > 0 ? update.pending_agents.join("<br />") : "No Agents To Display",
        html: true,
        fullWidth: true,
      });
    }

    function showAgentsInstalledList(update) {
      $q.dialog({
        title: "Agents With The Update Installed",
        message: update.installed_agents.length > 0 ? update.installed_agents.join("<br />") : "No Agents To Display",
        html: true,
        fullWidth: true,
      });
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
      pagination,

      // non-reactive data
      columns,

      // methods
      getWindowsUpdates,
      updateWindowsUpdates,
      editWindowsUpdate,
      showUpdateDetails,
      showAgentsPendingList,
      showAgentsInstalledList,
      notifySuccess,
      truncateText,
    };
  },
};
</script>