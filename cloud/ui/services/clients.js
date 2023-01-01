const API_URL = process.env.NUXT_ENV_API_URL;
const headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};


export const getClients = async () => {
  const response = await fetch(`${API_URL}/clients`, {
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


export const getClient = async (id) => {
  const response = await fetch(`${API_URL}/clients/${id}`, {
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


