const objectPath = require('object-path')

const deepGet = (obj, deepPath, defaultValue) => {
  let value = objectPath.get(obj, deepPath, defaultValue)
  if (value === undefined || value === null) value = ''
  return value
}

module.exports = {
  deepGet
}
