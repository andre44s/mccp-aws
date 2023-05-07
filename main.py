import streamlit as st
import boto3

ec2 = boto3.client('ec2', 
                   aws_access_key_id = st.secrets["aws_access_key_id"],
                   aws_secret_access_key = st.secrets["aws_secret_access_key"],
                   region_name=st.secrets["ec2_region_name"])

st.title("Minecraft Server Control Panel")
response = {}

col1, col2, col3 = st.columns(3)

with col1:
   if st.button("Turn On Server"):
      with st.spinner('Starting minecraft servers ...'):
         response = ec2.start_instances(InstanceIds=[st.secrets["main_server_id"]])
         st.success("Server is Starting")

with col2:
   if st.button("Turn Off Server"):
      with st.spinner('Stopping minecraft servers ...'):
         response = ec2.stop_instances(InstanceIds=[st.secrets["main_server_id"]])
         st.success("Server is Stopping")

with col3:
   if st.button("Check Server"):
      with st.spinner('Checking server availability ...'):
         response = ec2.describe_instances(InstanceIds=[st.secrets["main_server_id"]])
         try:
            instance_details = {}
            instance_details['launchTime'] = response['Reservations'][0]['Instances'][0]['LaunchTime'].strftime('%Y-%m-%dT%H:%M:%SZ')
            instance_details['availabilityZone'] = response['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']
            instance_details['publicDnsName'] = response['Reservations'][0]['Instances'][0]['PublicDnsName']
            instance_details['publicIpAddress'] = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
            instance_details['instanceState'] = response['Reservations'][0]['Instances'][0]['State']['Name']
            instance_details['minecraftDNS'] = instance_details['publicDnsName'] + ":" + st.secrets["minecraft_port"]
            response = instance_details
         except Exception as e:
            st.warning(f'Server is Off: {e}')
         
st.json(response)