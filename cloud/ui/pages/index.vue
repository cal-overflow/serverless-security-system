<template>
  <div>
    <grid-view title="System Overview">
      <camera-overview-card :cameras="cameras" />
      <user-overview-card :users="users" />
      <footage-preview-card subtext="with activity captured this month" :footage-count="activeFootageCount" />
    </grid-view>
  </div>
</template>

<script>
import { getClients } from '@/services/clients.js';
import { getUsers } from '@/services/users.js';
import { getVideoCount } from '@/services/videos.js';

export default {
  name: 'IndexPage',
  middleware: 'authenticate',
  async asyncData({ user }) {

    const tasks = [
      getClients(),
      getUsers(),
      getVideoCount('activity', {}),
    ];

    const [clients, users, activeFootageCount] = await Promise.all(tasks)

      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
      });

    return {
      cameras: clients,
      users,
      activeFootageCount,
      authenticatedUser: user
    };
  },
};
</script>
