import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [react()],
// })

export default {
  server: {
    host: true,
  },
};



// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
// export default defineConfig({
//     plugins: [react()],
//     server: {
//         host: true,
//         port: 3000
//     },
//     preview: {
//         host: true,
//         port: 3000
//     }
// })