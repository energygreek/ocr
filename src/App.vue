<template>
  <div id="app">
    <div class="header">
      <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/ocr">OCR</router-link> |
        <router-link to="/draw">Draw</router-link> |
        <router-link to="/about">About</router-link> |
        <a href="https://support.qq.com/product/750718" target="_blank">External</a> |
      </nav>
      <div class="controls">
        <input type="range" id="hue-slider" min="0" max="360" v-model="hue_value">
        <input type="number" id="hue-value" placeholder="value" v-model="hue_value">
        <svg @click="dark" id="dark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512">
          <path
            d="M223.5 32C100 32 0 132.3 0 256S100 480 223.5 480c60.6 0 115.5-24.2 155.8-63.4c5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6c-96.9 0-175.5-78.8-175.5-176c0-65.8 36-123.1 89.3-153.3c6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z" />
        </svg>
      </div>
    </div>
    <router-view />
  </div>
</template>

<script>
export default {
  data () {
    return {
      hue_value: 0
    }
  },
  methods: {
    dark () {
      document.body.classList.toggle('dark')
    }
  },
  watch: {
    hue_value (newValue) {
      document.documentElement.style.setProperty('--hue', newValue)
    }
  }
}
</script>

<style>
#app {
  font-family: sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding: 10px;
}

.controls {
  align-self: flex-end;
  /* right-align controls */
  margin-top: 10px;
}

@media (min-width: 768px) {
  .header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .controls {
    margin-top: 0;
  }
}
</style>
