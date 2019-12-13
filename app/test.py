import ipaddress
import utilities.cloudUtility

if __name__ == "__main__":
    msg = utilities.cloudUtility.CheckAzureIPs("13.73.16.129")
    print(msg)

    msg = utilities.cloudUtility.CheckAWSIPs("18.208.0.0")
    print(msg)

    msg = utilities.cloudUtility.CheckGithubIPs("192.30.252.0")
    print(msg)

    msg = utilities.cloudUtility.CheckGCPIPs("8.35.200.0")
    print(msg)