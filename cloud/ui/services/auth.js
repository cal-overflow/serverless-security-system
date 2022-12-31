const API_URL = process.env.NUXT_ENV_API_URL;
const headers = {'Content-Type': 'application/json', 'Accept': 'application/json'};


export const login = async (body) => {

  const response = await fetch(`${API_URL}/auth/login`,
    {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
    }
  );

  if (!response.ok) {
    throw new Error(await response.text())
  }

  const authInfo = await response.json();
  localStorage.setItem('accessToken', authInfo.access_token);
};

export const refreshToken = async () => {
  const accessToken = localStorage.getItem('accessToken');

  const response = await fetch(`${API_URL}/auth/refresh`,
    {
      method: 'POST',
      headers: {
        ...headers,
        'access-token': accessToken
      }
    }
  );

  console.log(response);

  if (!response.ok) {
    throw new Error(await response.text())
  }

  const authInfo = await response.json();
  localStorage.setItem('accessToken', authInfo.access_token);
};
