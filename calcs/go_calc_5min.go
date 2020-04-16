// You can edit this code!
// Click here and start typing.
package main

// mypath = "/home/gtserver/code/repos/stocks/data/raw/5min"
// calc_path = "/home/gtserver/code/repos/stocks/data/calcd/5min"


import (
  "fmt"
  "os"
  "path/filepath"
)




func main() {
    f_path := "/home/gtserver/code/repos/stocks/data/raw/5min"
    // var fs []string
    filepath.Walk(f_path, func(path string, info os.FileInfo, err error) error {
        // append(fs, filepath.Join(f_path, info.Name()))
        fmt.Println(filepath.Join(f_path, info.Name()))
        return nil
    })
    // fmt.Println(fs)
}