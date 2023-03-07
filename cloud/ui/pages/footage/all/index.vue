<template>
  <div></div>
</template>

<script>
const formatNumber = (num) => {
  return num.toLocaleString('en-US', {
    minimumIntegerDigits: 2,
    useGrouping: false
  });
};


const today = new Date();

export default {
  name: 'IndexPage',
  middleware: 'authenticate',
  asyncData({ redirect}) {
    redirect(`/footage/all/${today.getFullYear()}-${formatNumber(today.getMonth() + 1)}-${formatNumber(today.getDate())}`);

  }
}
</script>
