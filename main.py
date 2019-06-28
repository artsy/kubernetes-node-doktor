import time, os, re, sys, datetime

import pykube
from urllib3.exceptions import ProtocolError
from requests.exceptions import ConnectionError as ReqConnectionError

NODENAME = os.environ.get("NODENAME")
KUBECONFIG = os.environ.get("KUBECONFIG", "~/.kube/config")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "60"))

MATCH_EVENTS = [
  "rpc error",
  "failed create pod sandbox",
  "context deadline exceeded"
]

def log(msg):
  print("\n[%s] %s" %(datetime.datetime.now(), msg))

def main():
  if NODENAME is None:
    raise Exception("NODENAME cannot be None")

  api = pykube.HTTPClient(pykube.KubeConfig.from_file(KUBECONFIG))

  sys.stdout.write("Der node doktor ist in für %s, checkup every %s seconds..." % (NODENAME, POLL_INTERVAL))

  while True:
    try:
      bad_pods = []

      for pod in pykube.Pod.objects(api).filter(field_selector={"spec.nodeName": NODENAME, "status.phase": "ContainerCreating"}):
        for pod_event in pykube.Event.objects(api).filter(field_selector={"involvedObject.name": pod.obj['metadata']['name']}):
          for event in MATCH_EVENTS:
            if re.search(event, pod_event.obj['message'], re.IGNORECASE):
              log("Found event '%s' for pod %s" % (pod_event.obj['message'], pod.obj['metadata']['name']))
              bad_pods.append(pod)
              break

      if bad_pods:
        log("Cordoning node and deleting pods...")
        pykube.Node.objects(api).get(name=NODENAME).cordon()
        for pod in bad_pods:
          pod.delete()

    except (ProtocolError, ConnectionResetError, ConnectionError, ReqConnectionError):
      log("Connection reset...")
      api = pykube.HTTPClient(pykube.KubeConfig.from_file(KUBECONFIG))
      continue

    sys.stdout.write('.')
    sys.stdout.flush()
    time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
  main()