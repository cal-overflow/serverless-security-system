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
  localStorage.setItem('tokenExpiration', authInfo.token_expiration);
};

export const refreshToken = async () => {
  const accessToken = localStorage.getItem('accessToken');
  const tokenExpirationStr = localStorage.getItem('tokenExpiration');

  const tokenExpiration = new Date(0).setUTCSeconds(Math.floor(parseFloat(tokenExpirationStr)));
  const currentTime = Math.floor(Date.now());

  if (tokenExpiration - currentTime > 43200) {
    return; // Do nothing if there is more than 12 hours before the token expires
  }

  const response = await fetch(`${API_URL}/auth/refresh`,
    {
      method: 'POST',
      headers: {
        ...headers,
        'access-token': accessToken
      }
    }
  );

  if (!response.ok) {
    throw new Error(await response.text())
  }

  const authInfo = await response.json();
  localStorage.setItem('accessToken', authInfo.access_token);
};


export const logout = async () => {
  const accessToken = localStorage.getItem('accessToken');
  const tokenExpirationStr = localStorage.getItem('tokenExpiration');

  const tokenExpiration = new Date(0).setUTCSeconds(Math.floor(parseFloat(tokenExpirationStr)));
  const currentTime = Math.floor(Date.now());

  if (tokenExpiration - currentTime < 0) {
    return; // Do nothing if the user's current auth token is expired
  }

  const response = await fetch(`${API_URL}/auth/logout`,
    {
      method: 'POST',
      headers: {
        ...headers,
        'access-token': accessToken
      }
    }
  );

  if (!response.ok) {
    throw new Error(await response.text())
  }

  localStorage.removeItem('accessToken');
  localStorage.removeItem('tokenExpiration');
};
