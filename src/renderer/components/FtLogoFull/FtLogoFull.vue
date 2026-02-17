<template>
  <img :src="logoSrc" alt="FreeTube Focus" class="ft-logo-full" />
</template>

<script setup>
import logoSrc from '../../assets/img/logo_full.png'
</script>

<style scoped>
.ft-logo-full {
  max-width: 100%;
  height: auto;
  display: block;
}
</style>
