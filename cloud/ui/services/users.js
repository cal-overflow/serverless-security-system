const API_URL = process.env.NUXT_ENV_API_URL;
const headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};


export const getUsers = async () => {
  const response = await fetch(`${API_URL}/users`, {
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


export const getUser = async (id) => {
  const response = await fetch(`${API_URL}/users/${id}`, {
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


export const editUser = async (id, user) => {
  const response = await fetch(`${API_URL}/users/${id}`, {
    headers: {
      ...headers,
      'access-token': localStorage.getItem('accessToken')
    },
    method: 'PATCH',
    body: JSON.stringify(user),
  });

  if (!response.ok) {
    throw new Error(await response.text())
  }

  return await response.json();
};


export const deleteUser = async (id) => {
  const response = await fetch(`${API_URL}/users/${id}`, {
    headers: {
      ...headers,
      'access-token': localStorage.getItem('accessToken'),
      method: 'DELETE',
    }
  });

  if (!response.ok) {
    throw new Error(await response.text())
  }

  return await response.json();
};
