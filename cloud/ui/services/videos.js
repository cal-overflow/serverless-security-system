const API_URL = process.env.NUXT_ENV_API_URL;
const headers = {
  'Content-Type': 'application/json',
  Accept: 'application/json',
};

export const getVideos = async (videoType = 'all', { date, camera, hours }) => {
  const options = {
    date,
    camera,
    hours,
  };
  // remove all undefined (unset) options
  Object.keys(options).forEach((key) =>
    options[key] === undefined ? delete options[key] : {}
  );

  const queryParams = new URLSearchParams(options).toString();

  const response = await fetch(
    `${API_URL}/videos/${videoType}?${queryParams}`,
    {
      headers: {
        ...headers,
        'access-token': localStorage.getItem('accessToken'),
      },
      method: 'GET',
    }
  );

  if (!response.ok) {
    throw new Error(await response.text());
  }

  const videos = await response.json();
  return videos;
};

export const getVideoCount = async (videoType = 'all', { month, camera }) => {
  const options = {
    month,
    camera,
  };
  // remove all undefined (unset) options
  Object.keys(options).forEach((key) =>
    options[key] === undefined ? delete options[key] : {}
  );

  const queryParams = new URLSearchParams(options).toString();

  const response = await fetch(
    `${API_URL}/video-count/${videoType}?${queryParams}`,
    {
      headers: {
        ...headers,
        'access-token': localStorage.getItem('accessToken'),
      },
      method: 'GET',
    }
  );

  if (!response.ok) {
    throw new Error(await response.text());
  }

  const videoCount = await response.json();
  return videoCount;
};
