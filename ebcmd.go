package main

// import "github.com/aws/aws-sdk-go"
import (
  "fmt"
  "os"
  "os/exec"
  // "bytes"
)

func main() {
  AVAILABLE_COMMANDS := [12]string{
    "CMD-ConfigDeploy",
    "CMD-SystemTailLogs",
    "CMD-RestartAppServer",
    "CMD-Startup",
    "CMD-AppDeploy",
    "CMD-PatchInstance",
    "CMD-TailLogs",
    "CMD-BundleLogs",
    "CMD-PublishLogs",
    "CMD-ImmutableDeploymentFlip",
    "CMD-PreInit",
    "CMD-SelfStartup",
  }

  // run if no argument is presented
  if len(os.Args) < 2 {
     fmt.Println("Please pass an argument from the list below:")
     print_commands(AVAILABLE_COMMANDS)
     os.Exit(1)
  }
  
  // Check if argument is valid, and set command if it is
  var COMMAND string
  for _, v := range AVAILABLE_COMMANDS {
      if v == os.Args[1] {
      	fmt.Println("Argument is valid")
      	COMMAND = os.Args[1]
      } 
  }

  // If command is not set (not valid) exit and print valid arguments
  if COMMAND == "" {
     fmt.Printf("Command %s is invalid, please pass an argument from the list below:\n", os.Args[1])
     print_commands(AVAILABLE_COMMANDS)
     os.Exit(1)
  }

  // Set EB Command Json String
  EB_CMD := fmt.Sprintf(`{
  "api_version" : "1.0",
  "request_id": "0",
  "command_name": "%s"
  }`, COMMAND)

 
  run_eb_cmd(EB_CMD)

}

func print_commands(arr [12]string) {
   for _, v := range arr {
     fmt.Printf("\t%s\n", v)
   }
}

//Function that takes a Json String and executes command_processor
func run_eb_cmd(str string) {
   fmt.Println("Running command")
   cmd_data := fmt.Sprintf("CMD_DATA='%s' ./command-processor -e", str)

   cmd := exec.Command("/bin/sh", "-c", cmd_data)
   cmd.Dir = "/opt/elasticbeanstalk/bin"
   out, err := cmd.Output()
   if err != nil {
     fmt.Printf("%s", err)
     return
   }

   fmt.Printf("\n%s\n", out)
}





