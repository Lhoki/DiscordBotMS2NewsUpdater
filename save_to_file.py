def save_to_file(latest_link):
  update_file = open("last_update.txt","r+")
  update_file.write(latest_link)
  update_file.close()

def delete_contents():
  open('last_update.txt', 'w').close()

def read_file():
  get_file = open("last_update.txt","r")
  store_link = get_file.read()
  return(store_link)