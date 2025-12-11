<template>
    <div class="ocr-container">
      <img :src="imageUrl" ref="img" @load="onImageLoad" />
      <div
        v-for="(box, i) in boxes"
        :key="i"
        class="ocr-box"
        :style="{
          top: box.top * scaleY + 'px',
          left: box.left * scaleX + 'px',
          width: box.width * scaleX + 'px',
          height: box.height * scaleY + 'px',
        }"
      >
        {{ box.text }}
      </div>
      <input type="file" @change="uploadImage" />
    </div>
  </template>

<script>
export default {
  data () {
    return {
      imageUrl: '',
      boxes: [],
      imgNaturalWidth: 1,
      imgNaturalHeight: 1,
      scaleX: 1,
      scaleY: 1
    }
  },
  methods: {
    uploadImage (event) {
      const file = event.target.files[0]
      this.imageUrl = URL.createObjectURL(file)
      const formData = new FormData()
      formData.append('image', file)
      fetch('http://localhost:8080/api/ocr', {
        method: 'POST',
        body: formData
      })
        .then((res) => res.json())
        .then((data) => {
          this.boxes = data
        })
    },
    onImageLoad () {
      const img = this.$refs.img
      this.imgNaturalWidth = img.naturalWidth
      this.imgNaturalHeight = img.naturalHeight
      this.scaleX = img.clientWidth / img.naturalWidth
      this.scaleY = img.clientHeight / img.naturalHeight
    }
  }
}
</script>

  <style scoped>
  .ocr-container {
    position: relative;
    display: inline-block;
  }
  .ocr-box {
    position: absolute;
    font-size: 12px;
    color: var(--accent-color);
    pointer-events: auto;
    user-select: text;
    white-space: nowrap;
  }
  </style>
