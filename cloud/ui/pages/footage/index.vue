<template>
  <div class="max-w-screen-lg mx-auto">
    <grid-view title="Footage">
      <!-- Footage with activity -->
      <footage-preview-card label="With activity" subtext="captured so far this month" :footage-count="activeFootageCount" />
      
      <!-- Footage without activity -->
      <footage-preview-card label="Without activity" subtext="captured so far this month*" :footage-count="normalFootageCount" />

      <!-- All Footage -->
      <footage-preview-card label="All footage" subtext="captured so far this month*" :footage-count="allFootageCount" />
    </grid-view>

    <div class="bg-card-light dark:bg-card-dark m-0 md:m-6 p-4 shadow-lg dark:shadow-shadow-dark hover:shadow-none hover:rounded motion-safe:animate-fade-in-fast transition">
      <div class="flex flex-wrap sm:flex-nowrap justify-between w-full">
        <p class="my-auto ">
          *Videos without motion are kept for {{daysKeepingMotionlessVideos}} days
        </p>

        <small>
          <nuxt-link to="/config" class="text-primary-light dark:text-primary-dark underline hover:no-underline">
            Edit configuration
          </nuxt-link>
        </small>
      </div>
    </div>
    <card>
    </card>
  </div>
</template>

<script>
import { getConfig } from '@/services/config.js';
import { getVideoCount } from '@/services/videos.js';

export default {
  name: 'IndexPage',
  middleware: 'authenticate',
  async asyncData() {
    const tasks = [
      getVideoCount('normal', {}),
      getVideoCount('activity', {}),
      getConfig(),
    ];

    const [normalFootageCount, activeFootageCount, config] = await Promise.all(tasks)
      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
      });

    return {
      normalFootageCount,
      activeFootageCount,
      allFootageCount: normalFootageCount + activeFootageCount,
      daysKeepingMotionlessVideos: config.days_to_keep_motionless_videos,
    };
  },
};
</script>
