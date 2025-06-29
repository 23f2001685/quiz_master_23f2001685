<template>
        <!-- Example: Place this in your App.vue or a global layout -->
    <div class="toast-container position-fixed end-0 top-0 p-3" style="z-index: 9999">
      <div id="app-toast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
          <strong class="me-auto" id="toast-title">Title</strong>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body" id="toast-body">
          Hello, world! This is a toast message.
        </div>
      </div>
    </div>
</template>

<script>
// Show a toast with custom title and message
function showToast(title, message) {
  document.getElementById('toast-title').textContent = title
  document.getElementById('toast-body').textContent = message
  const toastEl = document.getElementById('app-toast')
  const toast = new bootstrap.Toast(toastEl)
  toast.show()
}

export default {
  name: 'Toast',
  methods: {
    showToast(title, message) {
      showToast(title, message)
    }
  },
}

</script>
