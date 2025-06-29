<template>
  <div class="fab col" data-bs-toggle="tooltip" data-bs-placement="left" title="Add Subject" @click="handleClick">
      + Add {{ toAdd }}
  </div>
</template>

<script>
  export default {
    name: 'Fab',
    props: ['toAdd'],
    methods: {
      handleClick() {
        this.$emit('click');
      },
    },
  };
</script>

<style scoped>
  .fab {
  position: fixed;
  bottom: 30px;
  left: 47%;
  width: 120px;
  height: 40px;
  background: rgba(92, 89, 89, 0.35);
  border: 5px solid linear-gradient(229deg, rgba(37,150,190,1) 0%, rgba(209,160,245,1) 73%);
  box-shadow: 0 8px 32px 0 rgba(18, 19, 32, 0.557);
  backdrop-filter: blur( 8px );
  -webkit-backdrop-filter: blur( 8px );
  color: white;
  border-radius: 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 999;
}

.fab:hover {
  background: linear-gradient(229deg, rgba(209,160,245,0.4) 0%, rgba(92, 89, 89, 0.35) 73%);
}
</style>
