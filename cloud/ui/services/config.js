const API_URL = process.env.NUXT_ENV_API_URL;
const headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};


export const getConfig = async () => {
  const response = await fetch(`${API_URL}/config`, {
    headers: {
      ...headers,
      'access-token': localStorage.getItem('accessToken')
    }
  });

  if (!response.ok) {
    throw new Error(await response.text())
  }

  return await response.json();
};


export const updateConfig = async (updatedConfig) => {
  const response = await fetch(`${API_URL}/config`, {
    headers: {
      ...headers,
      'access-token': localStorage.getItem('accessToken')
    },
    method: 'POST',
    body: JSON.stringify(updatedConfig),
  });

  if (!response.ok) {
    throw new Error(await response.text())
  }

  return await response.json();
};

