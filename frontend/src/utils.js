import objectPath from 'object-path'

const utilsFunc = {
  deepGet (obj, deepPath, defaultValue) {
    let value = objectPath.get(obj, deepPath, defaultValue)
    if (value === undefined || value === null) value = ''
    return value
  },

  addObjectToLocalStorage (localStorageItemName, item, keyToCheck) {
    let localStorageItem = []
    localStorageItem = JSON.parse(localStorage.getItem(localStorageItemName))

    if (!localStorageItem) {
      // if localStorage array does not exist
      localStorageItem = []
      localStorageItem.unshift(item)
      localStorage.setItem(localStorageItemName, JSON.stringify(localStorageItem))
    } else if (localStorageItem.length) {
      let idx = localStorageItem.findIndex(obj => utilsFunc.deepGet(obj, keyToCheck) === utilsFunc.deepGet(item, keyToCheck))
      // if localStorage array exists and item already in it
      if (idx >= 0) {
        localStorageItem.splice(idx, 1)
        localStorageItem.unshift(item)
        localStorage.setItem(localStorageItemName, JSON.stringify(localStorageItem))
      } else {
        // if localStorage array exists and item not in it
        localStorageItem.unshift(item)
        localStorage.setItem(localStorageItemName, JSON.stringify(localStorageItem))
      }
    }
  },

  urlArgsParser (url) {
    let urlArgsObj = {}

    try {
      let urlArgs = url.split('?')[1].split('&')
      for (let i = 0; i < urlArgs.length; i++) {
        urlArgsObj[urlArgs[i].split('=')[0]] = urlArgs[i].split('=')[1]
      }
    } catch (err) {
      console.error(err)
    }
    return urlArgsObj
  }
}

export default utilsFunc
