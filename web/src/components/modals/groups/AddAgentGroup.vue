<template>
  <q-dialog ref="dialogRef">
    <q-card class="q-dialog-plugin" style="width: 60vw">
      <q-bar>
        Send {{ agent.hostname }} To Group
        <q-space />
        <q-btn dense flat icon="close" v-close-popup>
          <q-tooltip class="bg-white text-primary">Close</q-tooltip>
        </q-btn>
      </q-bar>
      <q-form @submit="submit">
        <q-card-section class="q-gutter-sm">
          <q-select outlined dense options-dense label="Groups" v-model="group" :options="group_options" />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn dense flat push label="Cancel" v-close-popup />
          <q-btn :loading="loading" dense flat push label="Add" color="primary" type="submit" />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script>
// composition imports
import { ref } from "vue";
import { useQuasar, useDialogPluginComponent } from "quasar";
import mixins from "@/mixins/mixins";
import { addGroupMember } from "@/api/groups";
import { notifySuccess, notifyError } from "@/utils/notify";

export default {
  name: "AddAgentGroup",
  mixins: [mixins],
  props: {
    agent: Object,
  },
  setup(props) {
    const $q = useQuasar();
    const { dialogRef, onDialogOK, onDialogHide } = useDialogPluginComponent();

    const state = ref({ agent: props.agent });
    const loading = ref(false);

    return {
      // reactive data
      state,
      loading,

      // quasar dialog
      dialogRef,
      onDialogHide,
    };
  },
  data() {
    return {
      group_options: [],
      group: null,
    };
  },
  methods: {
    getGroups() {
      this.$q.loading.show();
      this.$axios
        .get("/groups/")
        .then(r => {
          this.group_options = this.formatGroupOptions(r.data);
          this.$q.loading.hide();
        })
        .catch(() => {
          this.$q.loading.hide();
        });
    },
    async submit() {
      const data = {
        agent: this.agent.agent_id,
        group: this.group.value,
      };
      try {
        const result = await addGroupMember(data.agent, { group_id: data.group });
        result.status ? notifySuccess(result.message) : notifyError(result.message);
        store.dispatch("refreshDashboard");
      } catch (e) {
        console.error(e);
      }
    },
  },
  mounted() {
    this.getGroups();
  },
};
</script>