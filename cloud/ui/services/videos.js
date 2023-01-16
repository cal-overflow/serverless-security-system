const API_URL = process.env.NUXT_ENV_API_URL;
const headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};


export const getVideos = async (videoType='all', { date, camera, startHour, endHour }) => {
  const options = {
    date,
    camera,
    hours: startHour && endHour ? `${startHour}-${endHour}` : undefined,
  };
  // remove all undefined (unset) options
  Object.keys(options).forEach(key => options[key] === undefined ? delete options[key] : {});

  const queryParams = new URLSearchParams(options).toString();

  const response = await fetch(`${API_URL}/videos/${videoType}?${queryParams}`, {
    headers: {
      ...headers,
      'access-token': localStorage.getItem('accessToken')
    },
    method: 'GET'
  });

  if (!response.ok) {
    throw new Error(await response.text());
  }

  const videos = await response.json();
  return videos;
};

