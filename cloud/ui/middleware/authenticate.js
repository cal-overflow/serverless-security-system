import { refreshToken, getAuthenticatedUser } from '@/services/auth.js';

export default async function(context) {
  // Check that the user's auth token is valid and refresh it if necessary
  // Also attach the user information to the nuxt context object
  const accessToken = localStorage.getItem('accessToken');

  if (!accessToken) {
    console.log('NO ACCESS TOKEN IN STORAGE');
    return context.redirect('/login');
  }

  try {
    await refreshToken();
  }
  catch {
    console.log('AN ERROR OCCURRED REFRESHING TOKEN');
    return context.redirect('/login');
  }

  try {
    context.user = await getAuthenticatedUser();
  }
  catch {
    console.log('AN ERROR OCCURRED GETTING AUTH USER');
    return context.redirect('/login');
  }

}
