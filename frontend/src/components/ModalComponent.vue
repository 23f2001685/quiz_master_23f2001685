<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal-container">
      <h3 class="modal-title">{{ title }}</h3>
      <slot>

      </slot>
      <div class="modal-actions">
        <button class="btn btn-primary" @click="handleSave">Save</button>
        <button class="btn btn-secondary" @click="handleCancel">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalComponent',
  props: ['title', 'isVisible'],
  methods: {
    handleSave() {
      this.$emit('save');
    },
    handleCancel() {
      this.$emit('cancel');
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 80vw;
  max-width: 900px;
  height: auto;
}

.modal-title {
  margin-bottom: 20px;
  text-align: center;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 2em;
}

button {
  padding: 10px 20px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  width: 10vw;
}
</style>
