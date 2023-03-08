import { getVideos } from '@/services/videos.js';
import { getClients } from '@/services/clients.js';

export const getFootage = async ({ params, route, footageType }) => {
    const lastForwardSlashIndex = params.pathMatch.includes('/') ? params.pathMatch.lastIndexOf('/') : params.pathMatch.length;
    const anchorIndex = params.pathMatch.indexOf('#');
    const lastIndex = anchorIndex === -1 ? params.pathMatch.length : anchorIndex;
    const dateFilter = params.pathMatch.substring(lastForwardSlashIndex + 1, lastIndex + 1);

    const selectedCamera = route.query.camera;
    const startingVideoTime = route.query.time;
    let cameraFilter = '';

    const tasks = [
      getVideos(footageType, { date: dateFilter, hours: '0-8' }),
      getVideos(footageType, { date: dateFilter, hours: '9-16' }),
      getVideos(footageType, { date: dateFilter, hours: '17-23' }),
      getClients(),
    ];

    const [videosP1, videosP2, videosP3, cameras] = await Promise.all(tasks)
      .catch((err) => {
        // TODO - implement error handling
        console.log(err);
      });

    const videos = [...videosP1, ...videosP2, ...videosP3];
    let filteredVideos = [...videos];

    videos.forEach((video) => {
      video.time_formatted = video.time.replace(/-/g, ':');
    });


    if (selectedCamera) {
       filteredVideos = videos.filter(({ camera }) => camera === selectedCamera);
       cameraFilter = selectedCamera;
    }

    let selectedVideoIndex = 0;
    if (startingVideoTime) {
      selectedVideoIndex = filteredVideos.findIndex(({ time}) => time === startingVideoTime);
    }

    const selectedVideo = filteredVideos[selectedVideoIndex];
    const selectedVideoCamera = cameras.find(({ id }) => id === selectedVideo?.camera);

    return {
      originalFilter: {
        dateFilter,
        cameraFilter,
        footageType,
      },
      footageType,
      dateFilter,
      cameraFilter,
      videos,
      filteredVideos,
      selectedVideoIndex,
      cameras,
      startingVideoTime,
      selectedCamera,
      selectedVideo,
      selectedVideoCamera,
    };
};

