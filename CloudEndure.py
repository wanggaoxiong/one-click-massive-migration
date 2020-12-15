#!/usr/bin/python

# =================================================================================================
# 
# CloudEndure API full documentation can be found here - https://console.awscloudendure.cn/api_doc/apis.html#
#
# usage: CloudEndure_One_Click_Migration.py -u USERNAME -p PASSWORD -n HOSTNAME -j PROJECT_NAME
# 
# 
# Arguments:
#  
#   -u USERNAME, 	--username USERNAME
#                         user name for the CloudEndure account
#   -p PASSWORD, 	--password PASSWORD
#                         password for the CloudEndure account
#   -n HOSTNAME, 	--agentname HOSTNAME
#                         hostname of instance to migrate
#   -j PROJECT, 	--project PROJECT_NAME
#                         CloudEndure's project name
# 
# 
# Required inputs: CloudEndure username and password, target server name
# 
# Outputs: Will print to console the entire process:
#	1. CloudEndure Agent installation on the target server.
#	2. Blueprint settings.
#	3. Replication progress.
#	4. Target server launch progress.
# 
# 
# =================================================================================================

import requests
import os
import time
import argparse
import json
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

HOST = 'https://console.awscloudendure.cn'
input_file = '/tmp/temp_CE/d'

with open(input_file, 'r') as f_type:
    lines=f_type.readlines()
    for line in lines:
        line = line.strip()
        print line
        INSTANCE_TYPE = line
f_type.close()


#INSTANCE_TYPE = "c5.large"
SUBNET = 'subnet-xxxxxx'
SG = 'sg-xxxxxx'

WIN_FOLDER = "c:\\temp"
LINUX_FOLDER = "/tmp"


###################################################################################################
def main():

# This is the main function, call the other functions to do the following:
# 	1. CloudEndure Agent installation on the target server.
#	2. Blueprint settings.
#	3. Replication progress.
#	4. Target server launch progress.
# 
# Returns: 	nothing - will always exit

	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--user', required=True, help='User name')
	parser.add_argument('-p', '--password', required=True, help='Password')
	parser.add_argument('-j', '--project', required=True, help='Project name')
	parser.add_argument('-n', '--agentname', required=True, help='Name of server')
	
	args = parser.parse_args()
	
	installation_token = get_token(args)
        if installation_token == -1:
                print "Failed to retrieve project installation token"
                return -1
	
	machine_id, project_id = install_agent(args, installation_token)
	# Check if we were able to fetch the machine id
	if machine_id == -1:
		print "Failed to retrieve machine id"
		return -1

	# Check replication status, set blueprint while waiting for it to complete
	wait_for_replication(args, machine_id, project_id)
	
	# Setting the blueprint. Failing to do so won't fail the entire process
	if set_blueprint(args, machine_id, project_id) == -1:
		print "Failed to set blueprint"
			
	# Launch the target instance on the cloud
	launch_target_machine(args, machine_id, project_id)


###################################################################################################
def get_token(args):

# This function fetch the project installation token
# Usage: get_token(args)
#       'args' is script user input (args.user, args.password, args.agentname)
#
# Returns:      -1 on failure

        print "Fetching the installation token..."
        session, resp, endpoint = login(args)
        if session == -1:
                print "Failed to login"
                return -1

        project_name = args.project

        projects_resp = session.get(url=HOST+endpoint+'projects')
        projects = json.loads(projects_resp.content)['items']

        project = [p for p in projects if project_name==p['name']]
        if not project:
                print 'Error! No project with name ' + args.project+ ' found'
                return -1

        return project[0]['agentInstallationToken']

###################################################################################################

def install_agent(args, installation_token):

# This function makes the HTTPS call out to the CloudEndure API and waits for the replication to complete
# 
# Usage: wait_for_replicaiton(args, machine_id, project_id)
# 	'args' is script user input (args.user, args.password, args.agentname, args.project)
# 	
# 
# Returns: 	0 on success, -1 on failure

	# Check if it's a windows or not
	if os.name == 'nt': 
		# Make sure the temp folder exitts, the installer will run from it
		if not os.path.exists(WIN_FOLDER):
			os.mkdir(WIN_FOLDER)
		os.chdir(WIN_FOLDER)
		fname = 'installer_win.exe'
		cmd = 'echo | ' +fname + ' -t ' + installation_token + ' --no-prompt'
	else:
		os.chdir(LINUX_FOLDER)
		fname = 'installer_linux.py'
		cmd = 'sudo python ' +fname + ' -t ' + installation_token + ' --no-prompt'
		
	url = HOST + '/' + fname
	request = requests.get(url)
	open(fname , 'wb').write(request.content)
	
	ret = os.system(cmd)
	# Return value of agent installer should be 0 if succeded
	if ret != 0:
		print "Failed installing CloudEndure agent"
		return -1, -1
	
	session, resp, endpoint= login(args)
	
	if session == -1:
		print "Failed to login"
		return -1, -1
	
	# Fetch the CloudEndure project ID in order to locate the machine itself
	projects_resp = session.get(url=HOST+endpoint+'projects')
	projects = json.loads(projects_resp.content)['items']
	
	project_id = None
	machine_id = None
	
	# Fetch the CloudEndure machine ID in order monitor the replication progress and launch the target server		
	print 'Getting machine id...'
	for project in projects:
		project_id = project['id']	
		
		machines_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/machines')
		machines = json.loads(machines_resp.content)['items']

		machine_id = [m['id'] for m in machines if args.agentname.lower() == m['sourceProperties']['name'].lower()]

		if machine_id:
			break
			
	if not machine_id:
		print 'Error! No agent with name ' + args.agentname+ ' found'
		return -1, -1
	
	return machine_id[0].encode('ascii','ignore'), project_id
	
###################################################################################################	
def wait_for_replication(args, machine_id, project_id):

# This function makes the HTTPS call out to the CloudEndure API multiple times until replication to complete.
# Once it's done, the function will call set_blueprint in order to apply the blueprint settings before 
# launching the target server.
#
# Usage: wait_for_replicaiton(args, machine_id, project_id)
# 	'args' is script user input (args.user, args.password, args.agentname)
# 	'machine_id' is the CloudEndure replicatin machine ID
# 	'project_id' is the CloudEndure project ID
# 
# Returns: 	0 on success, -1 on failure

	# Looping until replication completes
	print "Waiting for Replication to complete"
	while True:
		session, resp, endpoint = login(args)
		if session == -1:
			print "Failed to login"
			return -1
		
		# Waiting for replication to start and the connection to establish
		while True:
			try:
				machine_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/machines/'+machine_id)
				replication_status = json.loads(machine_resp.content)['replicationStatus']
				break
			except:
				print "Replication has not started. Waiting..."
				time.sleep(10)
		
		# Waiting for replication to start and the coneection to establish
		while replication_status != 'STARTED':
			print "Replication has not started. Waiting..."
			time.sleep(120)
			machine_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/machines/'+machine_id)
			replication_status = json.loads(machine_resp.content)['replicationStatus']
		
		while True:
			try:
				replicated_storage_bytes = json.loads(machine_resp.content)['replicationInfo']['replicatedStorageBytes']
				total_storage_bytes = json.loads(machine_resp.content)['replicationInfo']['totalStorageBytes']
				break
			except:
				print "Replication has not started. Waiting..."
				time.sleep(60)
				machine_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/machines/'+machine_id)
		
		# Replication has started, looping until complete, printing progress		
		while True:
			try:
				last_consistency = json.loads(machine_resp.content)['replicationInfo']['lastConsistencyDateTime']
				backlog = json.loads(machine_resp.content)['replicationInfo']['backloggedStorageBytes']
				if backlog == 0:
					print "Replication completed. Target machine is launchable!"
					return 0
				else:
					print 'Replication is lagging. Backlog size is '+ str(backlog)
					time.sleep(30)
			except:
				if replicated_storage_bytes == total_storage_bytes:
					print "Finalizing initial sync. Waiting..."
					time.sleep(30)
				else:
	                                replicated_storage_bytes = json.loads(machine_resp.content)['replicationInfo']['replicatedStorageBytes']
	                                total_storage_bytes = json.loads(machine_resp.content)['replicationInfo']['totalStorageBytes']

					print 'Replicated '+ str(replicated_storage_bytes/1024/1024)+' MB out of '+str(total_storage_bytes/1024/1024)+' MB bytes'
					print "Will check again in 1 minutes. Waiting..."
					time.sleep(60)				
			machine_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/machines/'+machine_id)			

###################################################################################################

def set_blueprint(args, machine_id, project_id):

# This function makes the HTTPS call out to the CloudEndure API to set the serve blueprint before launching it on Cloud
# This function will set the instanceType, subnetID, and the securityGroupIDs.
# 
# Usage: set_blueprint(args, machine_id, project_id)
# 	'args' is script user input (args.user, args.password, args.agentname)
# 	'machine_id' is the CloudEndure replicatin machine ID
# 	'project_id' is the CloudEndure project ID
# 
# Returns: 	0 on success, -1 on failure

	print "Setting blueprint..."
	session, resp, endpoint = login(args)
	if session == -1:
		print "Failed to login"
		return -1
	
	blueprints_resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/blueprints')
	blueprints = json.loads(blueprints_resp.content)['items']
	
	blueprint = [bp for bp in blueprints if machine_id==bp['machineId']]
	if len(blueprint) == 0:
		return -1		
	
	blueprint = blueprint[0]	
	
	blueprint['instanceType']=INSTANCE_TYPE
	###blueprint['subnetIDs']=[SUBNET]
	###blueprint['securityGroupIDs']=[SG]
	blueprint['machineId']=machine_id
	
	resp = session.patch(url=HOST+endpoint+'projects/'+project_id+'/blueprints/'+blueprint['id'],data=json.dumps(blueprint))
	if resp.status_code != 200:
		print 'Error setting blueprint!'
		print resp.status_code
		print resp.reason
		print resp.content
		return -1
		
	print "Blueprint was set successfully"
	return 0

	

###################################################################################################		
def launch_target_machine(args, machine_id, project_id):

# This function makes the HTTPS call out to the CloudEndure API and launches the target server on the Cloud
# 
# Usage: launch_target_machine(args, machine_id, project_id)
# 	'args' is script user input
# 	'machine_id' is the CloudEndure replicatin machine ID
# 	'project_id' is the CloudEndure project ID
# 
# Returns: 0 on success

	print "Launching target server"
	session, resp, endpoint = login(args)
	if session == -1:
		print "Failed to login"
		return -1
	items = {'machineId': machine_id}
	resp = session.post(url=HOST+endpoint+'projects/'+project_id+'/launchMachines', data=json.dumps({'items': [items], 'launchType': 'TEST'}))
	if resp.status_code != 202:
		print 'Error creating target machine!'
		print 'Status code is: ', resp.status_code
		return -1
	jobId = json.loads(resp.content)['id']


	isPending = True
	log_index = 0
	print "Waiting for job to finish..."
	while isPending:
		resp = session.get(url=HOST+endpoint+'projects/'+project_id+'/jobs/'+jobId)
		job_status = json.loads(resp.content)['status']
		isPending = (job_status == 'STARTED')
		job_log = json.loads(resp.content)['log']
		while log_index < len(job_log):
			if 'cleanup' not in job_log[log_index]['message']:
				if 'security group' not in job_log[log_index]['message']:
					print job_log[log_index]['message']
			log_index += 1
		
		time.sleep(5)

	print 'Target server creation completed!'
	return 0;

###################################################################################################	
def login(args):

# This function makes the HTTPS call out to the CloudEndure API to login using the credentilas provided
# 
# Usage: login(args)
# 	'args' is script user input (args.user, args.password, args.agentname)
# 
# Returns: 	-1 on failure
#			session, response, endpoint on success

	endpoint = '/api/latest/'
	session = requests.Session()
	session.headers.update({'Content-type': 'application/json', 'Accept': 'text/plain'})
	resp = session.post(url=HOST+endpoint+'login', data=json.dumps({'username': args.user, 'password': args.password}))
	if resp.status_code != 200 and resp.status_code != 307:
		print "Bad login credentials"
		return -1, -1, -1
	#print 'Logged in successfully'	

	
	# Check if need to use a different API entry point and redirect
	if resp.history:
		endpoint = '/' + '/'.join(resp.url.split('/')[3:-1]) + '/'
		resp = session.post(url=HOST+endpoint+'login', data=json.dumps({'username': args.user, 'password': args.password}))
	
	try:
		session.headers.update({'X-XSRF-TOKEN' : resp.cookies['XSRF-TOKEN']})
	except:
		pass
	
	return session, resp, endpoint
	
###################################################################################################		
if __name__ == '__main__':
    main()

