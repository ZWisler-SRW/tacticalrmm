<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="width: 60vw">
      <q-bar>
        {{ `${group.name} Properties` }}
        <q-space />
        <q-btn dense flat icon="close" v-close-popup>
          <q-tooltip class="bg-white text-primary">Close</q-tooltip>
        </q-btn>
      </q-bar>
      <q-form @submit="submit">
        <q-card-section>
          <q-input :rules="[val => !!val || 'Name is required']" outlined dense v-model="state.name" label="Name" />
        </q-card-section>

        <q-card-actions align="right">
          <q-btn dense flat push label="Cancel" v-close-popup />
          <q-btn :loading="loading" dense flat push label="Save" color="primary" type="submit" />
        </q-card-actions>
      </q-form>
    </q-card>
  </q-dialog>
</template>

<script>
// composition imports
import { ref, onMounted } from "vue";
import { useQuasar, useDialogPluginComponent } from "quasar";
import { editGroup } from "@/api/groups";
import { notifySuccess, notifyError } from "@/utils/notify";

export default {
  name: "GroupPropertiesForm",
  emits: [...useDialogPluginComponent.emits],
  props: {
    group: Object,
  },
  setup(props) {
    // setup quasar dialog
    const $q = useQuasar();
    const { dialogRef, onDialogOK, onDialogHide } = useDialogPluginComponent();

    const state = !!props.group ? ref(Object.assign({}, props.group)) : ref({ group: props.id, name: "" });
    const loading = ref(false);

    async function submit() {
      loading.value = true;
      const data = {
        group: state.value,
      };
      try {
        const result = !!props.group ? await editGroup(props.group.id, data.group) : await saveGroup(data.group);
        result.status ? notifySuccess(result.message) : notifyError(result.message);
        onDialogOK();
      } catch (e) {
        console.error(e);
      }
      loading.value = false;
    }

    onMounted(async () => {
      $q.loading.show();
      try {
      } catch (e) {
        console.error(e);
      }
      $q.loading.hide();
    });

    return {
      // reactive data
      state,
      loading,

      // methods
      submit,

      // quasar dialog
      dialogRef,
      onDialogHide,
    };
  },
};
</script>