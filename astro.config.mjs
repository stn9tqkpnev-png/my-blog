// @ts-check
import { unified } from '@astrojs/markdown-remark';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { defineConfig, fontProviders } from 'astro/config';

export default defineConfig({
  trailingSlash: 'always',
  redirects: {
    '/category/スマートウォッチ/': '/category/smartwatch/',
    '/category/スマートホーム/': '/category/smarthome/',
    '/category/アプリ/': '/category/app/',
    '/category/買い物/': '/category/shopping/',
  },
  image: { service: { entrypoint: 'astro/assets/services/noop' } },
  markdown: { processor: unified() },
  site: 'https://workbench-note.com',
  integrations: [mdx(), sitemap()],
  fonts: [
    {
      provider: fontProviders.local(),
      name: 'Atkinson',
      cssVariable: '--font-atkinson',
      fallbacks: ['sans-serif'],
      options: {
        variants: [
          { src: ['./src/assets/fonts/atkinson-regular.woff'], weight: 400, style: 'normal', display: 'swap' },
          { src: ['./src/assets/fonts/atkinson-bold.woff'], weight: 700, style: 'normal', display: 'swap' },
        ],
      },
    },
  ],
});
