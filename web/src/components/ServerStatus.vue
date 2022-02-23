<template>
  <q-card>
    <q-bar>
      <q-btn @click="getServerStatus" class="q-mr-sm" dense flat push icon="refresh" />Server Status
      <q-space />
      <q-btn dense flat icon="close" v-close-popup>
        <q-tooltip content-class="bg-white text-primary">Close</q-tooltip>
      </q-btn>
    </q-bar>
  </q-card>
</template>

<script>
// composition api
import { ref, onMounted } from "vue";
import { fetchServerInfo } from "@/api/server";

export default {
  name: "ServerStatus",
  components: {},
  props: {},
  setup(props) {
    // set main debug log functionality
    const loading = ref(false);
    const filter = ref("");
    const summary = null;

    async function getServerStatus() {
      summary = await fetchServerInfo();
      console.log(summary);
    }

    function diskBarColor(percent) {
      if (percent < 80) {
        return "positive";
      } else if (percent > 80 && percent < 95) {
        return "warning";
      } else {
        return "negative";
      }
    }

    const disks = computed(() => {
      console.log(summary);
    });

    // vue component hooks
    onMounted(() => {
      // Load server status, refresh every few seconds
      getServerStatus();
    });

    return {
      // data
      loading,
      filter,
      disks,

      // methods
      getServerStatus,
    };
  },
};
</script>