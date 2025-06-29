<template>
  <div>
    <h2>Draw Text Below</h2>
    <canvas ref="canvas" width="500" height="200"
            @mousedown="startDraw" @mousemove="draw" @mouseup="stopDraw" @mouseleave="stopDraw"
            style="border:1px solid #ccc; cursor: crosshair;"></canvas>

    <div style="margin-top: 10px;">
      <button @click="clearCanvas">Clear</button>
      <button @click="submitCanvas">Submit for OCR</button>
    </div>

    <div v-if="ocrResult">
      <h3>OCR Result:</h3>
      <pre>{{ ocrResult }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      drawing: false,
      ctx: null,
      ocrResult: ''
    }
  },
  mounted () {
    const canvas = this.$refs.canvas
    this.ctx = canvas.getContext('2d')
    this.ctx.fillStyle = '#fff'
    this.ctx.fillRect(0, 0, canvas.width, canvas.height)

    this.ctx.lineWidth = 3
    this.ctx.lineCap = 'round'
    this.ctx.strokeStyle = '#000'
  },
  methods: {
    startDraw (e) {
      this.drawing = true
      const rect = this.$refs.canvas.getBoundingClientRect()
      this.ctx.beginPath()
      this.ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top)
    },
    draw (e) {
      if (!this.drawing) return
      const rect = this.$refs.canvas.getBoundingClientRect()
      this.ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top)
      this.ctx.stroke()
    },
    stopDraw () {
      this.drawing = false
    },
    clearCanvas () {
      const canvas = this.$refs.canvas
      this.ctx.clearRect(0, 0, canvas.width, canvas.height)
    },
    submitCanvas () {
      this.ocrResult = ''
      const canvas = this.$refs.canvas
      canvas.toBlob(blob => {
        const formData = new FormData()
        formData.append('image', blob, 'handwritten.png')
        fetch('http://localhost:5000/draw', {
          method: 'POST',
          body: formData
        })
          .then(res => res.json())
          .then(data => {
            this.ocrResult = data.text || JSON.stringify(data)
          })
      }, 'image/png')
    }
  }
}
</script>
