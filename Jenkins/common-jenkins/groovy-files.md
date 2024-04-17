





## 1) pipeline basic sample



```groovy
def label = "jenkins-agent-${UUID.randomUUID().toString()}"
@Library("icis") _
 
podTemplate(label: label, serviceAccount: G_SA, namespace: G_NAMESPACE){
    node('maven-agent') {//TEMPLATE_LABEL
        container('build-tools') {
            stage('Clone Git Project') {
                sh icis.cloneGitProject()
            }
            stage('Merge Resource SafeDB') {
                sh icis.mergeResourceSafeDB()
            }
            stage('Add Git Tag') {
                sh icis.addGitTag("${P_TAG}")
            }
            stage('Maven Build & Image Push ') {
                sh icis.mvnBuild_ImgPush_AddAgent("${P_TAG}")
            }
        }
    }
}
```





## 2) podman ssample



```groovy


def label = "jenkins-agent-${UUID.randomUUID().toString()}"
@Library("icis") _

podTemplate(label: label, serviceAccount: G_SA, namespace: G_NAMESPACE){
	node('podman-agent') {//TEMPLATE_LABEL
		container('podman-agent') {
			stage('Clone Git Project') {
				sh icis.cloneGitProject()            
			}
				stage('Add Git Tag') {
				sh icis.addGitTag("${P_TAG}")
			}
			stage('Podman Build & Image Push ') {
				sh icis.podman_build("${P_TAG}")
			}
			stage('GitOps Update by ENVs') {
				sh icis.gitOpsUpdateByENVsDevPilotVer("${P_TAG}")
			}
		}
	}
}


```





## 2) icis.groovy

* 위치 : common-jenkins > vars > icis.groovy

```groovy
#!/usr/bin/env groovy

/*
		mvn clean compile deploy:deploy-file 
		-Durl=http://nexus.dev.icis.kt.co.kr/repository/common-repository 
		-Dfile=.\target\${P_PRJ_NM}-"""+version+""".jar 
		-Dpackaging=jar 
		-DgeneratePom=false 
		-DskipTests 
		-Drevision="""+version+""" 
		--settings ${G_MVN_SETTINGS_PATH}/settings_${P_DOMAIN}_admin.xml
		 -s /var/jenkins_home/maven/settings.xml
		*/

def moduleBuild(version){
	return """
		set +x
        		cd ${P_PRJ_NM}
        		mvn clean compile deploy -DskipTests -Dname=${P_PRJ_NM} -Drevision=${newVersion} --settings ${G_MVN_SETTINGS_PATH}/settings_${P_DOMAIN}_admin.xml
                
                echo '---------------------------'
                mvn versions:set -DnewVersion=${newVersion} --settings ${G_MVN_SETTINGS_PATH}/settings_${P_DOMAIN}_admin.xml
	"""
}

def moduleBuildOnlyJar(version){
	return """
		
		cd ${P_PRJ_NM}
		
		mvn clean install -Drevision="""+version+""" --settings ${G_MVN_SETTINGS_PATH}/settings_${P_DOMAIN}_admin.xml
		ls target
		mvn -X deploy:deploy-file -DgroupId=com.kt.icis -DartifactId=${P_PRJ_NM} -Dversion="""+version+""" -Dpackaging=jar -DgeneratePom=false -Dfile=target/${P_PRJ_NM}-"""+version+""".jar -Durl=http://nexus.dev.icis.kt.co.kr/repository/common-repository -DrepositoryId=common-lib --settings ${G_MVN_SETTINGS_PATH}/settings_${P_DOMAIN}_admin.xml
	"""
}

def moduleBuildOnlyPom(){
	return """
	                cd ${P_PRJ_NM}
                mvn -X deploy:deploy-file -DgroupId=com.kt.icis -DartifactId=${P_ARTIFACT_ID} -Dversion=${P_VERSION} -Dpackaging=pom -DgeneratePom=false -Dfile=./${P_ARTIFACT_ID}-${P_VERSION}.pom -Durl=http://nexus.dev.icis.kt.co.kr/repository/common-repository -DrepositoryId=common-lib --settings ${G_MVN_SETTINGS_PATH}/settings_${P_DOMAIN}_admin.xml
	"""
}
//ls ${G_MVN_SETTINGS_PATH}/repository/${P_LIB_PATH}
def cleanM2Folder(){
	if("${P_LIB_PATH}"=='')
		throw new Exception("You must insert the Library path")
	else
		sh """
			if ! test -d ${G_MVN_SETTINGS_PATH}/repository/${P_LIB_PATH}; then
				echo "${P_LIB_PATH} : Not found the directory."
				return "1"
			else
				cd ${G_MVN_SETTINGS_PATH}/repository
				rm -rf ./${P_LIB_PATH}
				echo "${P_LIB_PATH} Clean Success"
			fi
		"""
}

def cloneGitProject(){
	return """
		set +x
		git clone -b ${P_BRANCH} https://gitlab-ci-token:${G_GIT_TOKEN}@gitlab.dspace.kt.co.kr/${P_PRJ_PATH}/${P_PRJ_NM}.git
		echo "Build from ${P_BRANCH} Branch !!!"
	"""
}

//elstic agent 리소스 추가.
def mergeResourceSafeDB(){
	return """
		set +x 
		cp -r ${G_MVN_SETTINGS_PATH}/resources/*  ${P_PRJ_NM}/src/main/resources/
		cp -r ${G_MVN_SETTINGS_PATH}/jar/  ${P_PRJ_NM}/src/main/resources/
	"""
}

def mergeResourceSafeDBbill(){
	return """
		set +x 
		cp -r ${G_MVN_SETTINGS_PATH}/resources/  ${P_PRJ_NM}/src/main/resources/
	"""
}


def mergeResourceOnlySafeDB(){
	return """
		set +x
		cp -r ${G_MVN_SETTINGS_PATH}/resources/*  ${P_PRJ_NM}/src/main/resources/
	"""
}

def mergeResourceElasticStack(){
	return """
		set +x
		cp -r ${G_MVN_SETTINGS_PATH}/jar/  ${P_PRJ_NM}/src/main/resources/
	"""
}

def addGitTag(){
	return """
		set +x
		cd ${P_PRJ_NM}
		git config --global user.email "sa-admin@kt.com"
		git config --global user.name "sa-admin"
		git tag ${P_TAG} -m "${P_TAG_MSG}" -f
		git push origin ${P_TAG} -f
	"""
}

def addGitTag(tag1){
            def num = ''
            if(tag1 == "dev" || P_BRANCH == "develop") {
                def data = new Date()
                def dataFormat = data.format("yyyyMMddHHmmss")
                num = dataFormat
                print "time tag newVersion ---${num}---"
            }	
            def numlen = num.replace(".","").length()
            if (numlen  > 10) {
                label = num
                print "${num} time tag newVersion ${label}"
            	return """
            		set +x
            		cd ${P_PRJ_NM}
            		git config --global user.email "sa-admin@kt.com"
            		git config --global user.name "sa-admin"
            		git tag ${label} -m "${P_TAG_MSG}" -f
            		git push origin ${label} -f
            	"""
            } else {
                def Array= []
                def TagArray= []
                def Tag_VERSION = "${P_BRANCH}".split('/')[1]
                def P_IMG = "${P_IMG_FULL_NM}".split('/')[1]
                def tag = ""
                def ctokenform = ""
                def ctoken = ""
                def newctokenform = ""
                def newctoken = ""
                def newVersion = ""
                ctokenform = sh returnStdout:true, script:"""curl -u  icistr-sa:icistr-sa -X GET 'https://nexus.dspace.kt.co.kr/service/rest/v1/search?repository=docker-dspace-host&name=${P_IMG_FULL_NM}'| jq '.continuationToken' """
                ctoken = ctokenform.replace('"',"").replace("\n","")
                print "ctoken ----${ctoken}----"
                
                tag = sh returnStdout:true, script:"""curl -u  curl -u icistr-sa:icistr-sa -X GET 'https://nexus.dspace.kt.co.kr/service/rest/v1/search?repository=docker-dspace-host&name=${P_IMG_FULL_NM}' |  jq '.items[] | select(.version | contains("${Tag_VERSION}")).version' | sort -V | tail -n 1 """
				
                if (tag) {
                  TagArray.add(tag)
                  print "TagArray ${TagArray}"
                }
                while (ctoken != "null") {

                    tag = sh returnStdout:true, script:"""curl -u  curl -u icistr-sa:icistr-sa -X GET 'https://nexus.dspace.kt.co.kr/service/rest/v1/search?repository=docker-dspace-host&name=${P_IMG_FULL_NM}&continuationToken=${ctoken}'| jq -r '.items[] | select(.version | contains("${Tag_VERSION}")).version' | sort -V | tail -n 1 """
                    if (tag) {
                      TagArray.add(tag)
                      print "TagArray ${TagArray}"
                    }
                    newctoken1 = sh returnStdout:true, script:"""curl -u  icistr-sa:icistr-sa -X GET 'https://nexus.dspace.kt.co.kr/service/rest/v1/search?repository=docker-dspace-host&name=${P_IMG_FULL_NM}&continuationToken=${ctoken}'| jq '.continuationToken' """
                    print "newctoken1 ----${newctoken1}----"
                    
                    newctoken = newctoken1.replace('"',"").replace("\n","")
                    print "newctoken ----${newctoken}----"
                    if (newctoken != "null"){
                        ctoken = newctoken
                        print "ctoken = newctoken ----${ctoken}----"
                        
                        tag = sh returnStdout:true, script:"""curl -u  curl -u icistr-sa:icistr-sa -X GET 'https://nexus.dspace.kt.co.kr/service/rest/v1/search?repository=docker-dspace-host&name=${P_IMG_FULL_NM}&continuationToken=${ctoken}'| jq -r '.items[] | select(.version | contains("${Tag_VERSION}")).version' | sort -V | tail -n 1 """
                        if (tag) {
                          TagArray.add(tag)
                          print "TagArray ${TagArray}"
                        }
                        newctokenform = sh returnStdout:true, script:"""curl -u  curl -u icistr-sa:icistr-sa -X GET 'https://nexus.dspace.kt.co.kr/service/rest/v1/search?repository=docker-dspace-host&name=${P_IMG_FULL_NM}&continuationToken=${ctoken}'| jq '.continuationToken' """
                        
                        newctoken = newctokenform.replace('"',"").replace("\n","")
                        print "newctoken ----${newctoken}----"
                    } else {
                      ctoken = "null"
                    }
                }
                
                if (TagArray) {
                    tag = TagArray.reverse()[0]
                    print "tag = TagArray.reverse()[0] ${tag}"
                }
                def branch = P_BRANCH.split("/")[1]
                if (tag){
                    def tagParts = tag.replace('"',"").replace("\n","")
                    print "tagParts : ---${tagParts}---"
                    index = tagParts.indexOf(".")

                    for (int i = 0; i < 2; i++ ){
                        index = tagParts.indexOf(".", index + 1)
                }
                    bugfix = tagParts.substring(index + 1) as int
                    bugfix=bugfix + 1			
                    newVersion = "${branch}.${bugfix}"
                    print "newVersion ${newVersion}"
                } else {
                    newVersion = "${branch}.1"
                    print "newVersion ${newVersion}"
                }
                label = newVersion
	        return """
                set +x
            		cd ${P_PRJ_NM}
            		git config --global user.email "sa-admin@kt.com"
            		git config --global user.name "sa-admin"
            		git tag ${newVersion} -m "${P_TAG_MSG}" -f
            		git push origin ${newVersion} -f
	        """
            }
}


def getGitOpsUpdateStr(env){
	return """
		set +x
		mkdir """+env+"""
		cd """+env+"""
		git clone https://gitlab-ci-token:${G_GIT_TOKEN}@gitlab.dspace.kt.co.kr/${P_GITOPS_PATH}/${P_GITOPS_NM}-"""+env+""".git
		git config --global user.email "sa-admin@kt.com"
		git config --global user.name "sa-admin"
		cd ${P_GITOPS_NM}-"""+env+"""/${P_PRJ_NM}/kustomize
		git checkout HEAD
		kustomize edit set image nexus.dspace.kt.co.kr/${P_IMG_FULL_NM}:${P_TAG}
		git add .
		git commit -am 'update image tag ${P_TAG} from ICIS-TR_Jenkins'
					
		git push origin HEAD

	"""
}
/* 23.06.07 rest-gateway 수정*/
def getGitOpsUpdateStr(tag,env){
	try {
		sh """
		    echo 'try outside 2 ==========>'
			set +x
			mkdir """+env+"""
			cd """+env+"""
			git clone https://gitlab-ci-token:${G_GIT_TOKEN}@gitlab.dspace.kt.co.kr/${P_GITOPS_PATH}/${P_GITOPS_NM}-"""+env+""".git
			git config --global user.email "sa-admin@kt.com"
			git config --global user.name "sa-admin"

			cd ${P_GITOPS_NM}-"""+env+"""/${P_PRJ_NM}/kustomize
			git checkout HEAD
			kustomize edit set image nexus.dspace.kt.co.kr/${P_IMG_FULL_NM}:"""+tag+"""
			git add .
			git commit -am 'update image tag  """+tag+""" from ICIS-TR_Jenkins'
			
			echo 'git push --dry-run origin HEAD ==========>'	
			git push --dry-run origin HEAD

			echo 'git push --force origin HEAD ==========>'			
			git push --force origin HEAD
		"""
	} catch(e) {
		try {
			sh """
			    echo 'try inside 1 ==========>'	
				set +x
				sleep 10
				cd ${P_ENVS}/${P_GITOPS_NM}-"""+env+"""/${P_PRJ_NM}/kustomize
				git checkout HEAD
				echo 'git reset --hard origin/main ==========>'		
				git reset --hard origin/main

				echo 'git pull origin HEAD ==========>'	
				git pull origin HEAD

				echo 'pwd ==========>'	
				pwd

				echo 'ls ==========>'	
				ls

				echo 'cat kustomization.yaml | grep newTag ==========>'
				cat kustomization.yaml | grep newTag

				echo 'kustomize edit set image tag ${P_IMG_FULL_NM} ==========>'
				kustomize edit set image nexus.dspace.kt.co.kr/${P_IMG_FULL_NM}:"""+tag+"""

				git add .
				git commit -am 'update image tag  """+tag+""" from ICIS-TR_Jenkins'

				echo 'tag ${tag} ==========>'	

				echo 'git push --force origin HEAD ==========>'
				git push --force origin HEAD
			"""
			
		} catch (ex) {
			try{
				sh """
					echo 'catch inside 1 ==========>'
					set +x
					sleep 20
					cd ${P_ENVS}/${P_GITOPS_NM}-"""+env+"""/${P_PRJ_NM}/kustomize
					git checkout HEAD
					echo 'git reset --hard origin/main ==========>'		
					git reset --hard origin/main

					echo 'git pull origin HEAD ==========>'	
					git pull origin HEAD

					echo 'pwd ==========>'	
					pwd

					echo 'ls ==========>'	
					ls

					echo 'cat kustomization.yaml | grep newTag ==========>'
					cat kustomization.yaml | grep newTag

					echo 'kustomize edit set image tag ${P_IMG_FULL_NM} ==========>'
					kustomize edit set image nexus.dspace.kt.co.kr/${P_IMG_FULL_NM}:"""+tag+"""

					git add .
					git commit -am 'update image tag  """+tag+""" from ICIS-TR_Jenkins'							

					echo 'tag ${tag} ==========>'	

					echo 'git push --force origin HEAD ==========>'
					git push --force origin HEAD
				"""
			} catch (exc) {
				sh """
					echo 'catch inside 1 ==========>'
					set +x
					sleep 20
					cd ${P_ENVS}/${P_GITOPS_NM}-"""+env+"""/${P_PRJ_NM}/kustomize
					git checkout HEAD
					echo 'git reset --hard origin/main ==========>'		
					git reset --hard origin/main

					echo 'git pull origin HEAD ==========>'	
					git pull origin HEAD

					echo 'pwd ==========>'	
					pwd

					echo 'ls ==========>'	
					ls

					echo 'cat kustomization.yaml | grep newTag ==========>'
					cat kustomization.yaml | grep newTag

					echo 'kustomize edit set image tag ${P_IMG_FULL_NM} ==========>'
					kustomize edit set image nexus.dspace.kt.co.kr/${P_IMG_FULL_NM}:"""+tag+"""

					git add .
					git commit -am 'update image tag  """+tag+""" from ICIS-TR_Jenkins'					

					echo 'tag ${tag} ==========>'	

					echo 'git push --force origin HEAD ==========>'
					git push --force origin HEAD
				"""
			}
		}
    }
	return """
		set +x
	"""
}

def gitTry(tag) {
	sh """
			set +x
			sleep 5
			cd ${P_ENVS}/${P_GITOPS_NM}-"""+env+"""/${P_PRJ_NM}/kustomize
			git checkout HEAD
			echo 'git reset --hard origin/main ==========>'		
			git reset --hard origin/main

			echo 'git pull origin HEAD ==========>'	
			git pull origin HEAD

			echo 'pwd ==========>'	
			pwd

			echo 'ls ==========>'	
			ls

			echo 'cat kustomization.yaml | grep newTag ==========>'
			cat kustomization.yaml | grep newTag

			echo 'tag ${tag} ==========>'	

			echo 'kustomize edit set image 1111 ==========>'
			kustomize edit set image nexus.dspace.kt.co.kr/${P_IMG_FULL_NM}:1111
			git add .
			git commit -am 'update image tag  from ICIS-TR_Jenkins'

			echo 'kustomize edit set image tag ==========>'
			kustomize edit set image nexus.dspace.kt.co.kr/${P_IMG_FULL_NM}:"""+tag+"""

			echo 'git add . ==========>'
			git add .
			
			echo 'git commit ==========>'
			git commit -am 'update image tag  """+tag+""" from ICIS-TR_Jenkins'

			echo 'git push --force origin HEAD ==========>'
			git push --force origin HEAD
		"""
}

def getGitOpsUpdateStrDevPilot(tag,env){
	return """
		set +x
		mkdir """+env+"""
		cd """+env+"""
		git clone https://gitlab-ci-token:${G_GIT_TOKEN}@gitlab.dspace.kt.co.kr/${P_GITOPS_PATH}/${P_GITOPS_NM}-"""+env+""".git
		git config --global user.email "sa-admin@kt.com"
		git config --global user.name "sa-admin"

		cd ${P_GITOPS_NM}-"""+env+"""/${P_PRJ_NM}/kustomize
		git checkout HEAD
		kustomize edit set image nexus.dspace.kt.co.kr/${P_IMG_FULL_NM}:"""+tag+"""
		git add .
		git commit -am 'update image tag  """+tag+""" from ICIS-TR_Jenkins'
					
		git push origin HEAD

	"""
}

def gitOpsUpdateByENVsDevPilotVer(tag2){
	print "newVersion ${label}"
	str=""
	envs="${P_ENVS}".tokenize(',')

	for(i in envs){
		str+=getGitOpsUpdateStrDevPilot(label,i)
	}
	return str
}



def gitOpsUpdateByENVs(){
	print "newVersion ${label}"
	str=""
	envs="${P_ENVS}".tokenize(',')
	for(i in envs){
		str+=getGitOpsUpdateStr(label,i)
	}
	return str
}

def gitOpsUpdateByENVs(tag2){
	print "newVersion ${label}"
	str=""
	envs="${P_ENVS}".tokenize(',')

	for(i in envs){
		str+=getGitOpsUpdateStr(label,i)
	}
	return str
}

def gitOpsUpdateByENVsDevPilot(tag){
	str=""
	envs="${P_ENVS}".tokenize(',')

	for(i in envs){
		str+=getGitOpsUpdateStrDevPilot(tag,i)
	}
	return str
}


/*
2023.04.20 mvnBuild_ImgPush_AddAgent사용하지않으며 
아래 내용 gitOps 로 이동
			-Djib.container.jvmFlags=-javaagent:/app/resources/elastic-apm-agent-1.36.0.jar,-Delastic.apm.service_name=my-service-name,-Delastic.apm.secret_token=,-Delastic.apm.server_url=http://apm.dev.icis.kt.co.kr,-Delastic.apm.environment=dev,-Delastic.apm.application_packages=com.kt.icis
*/
/*
 * 임시 */

def mvnBuild_ImgPush_AddAgent(tag){
            def num = ''
            if(tag == "dev" || P_BRANCH == "develop") {
                def data = new Date()
                def dataFormat = data.format("yyyyMMddHHmmss")
                num = dataFormat
                print "time tag newVersion ---${num}---"
				label = num
            }	
                print "newVersion ${label}"

                def JAVA_OPTS = "-javaagent:/app/resources/jar/elastic-apm-agent-1.39.0.jar -Delastic.apm.service_version=${label} -Delastic.apm.service_name=${P_PRJ_NM} -Delastic.apm.secret_token= -Delastic.apm.application_packages=com.kt.icis"
				def appFull = sh returnStdout:true, script:"""ls ${P_PRJ_NM}/src/main/java | grep -r @SpringBootApplication"""
				print "${appFull}"
				def appFulljava = "${appFull}".split("java/")[1]				
				print "${appFulljava}"
				def appSp="${appFulljava}".split(".java")[0]
				print "${appSp}"
				def app = appSp.replace("/",".")
				print "${app}"
                return """
                set +x
        	    cd ${P_PRJ_NM}
                mvn clean package jib:build -DskipTests --settings ${G_MVN_SETTINGS_PATH}/settings_${P_DOMAIN}.xml \
        			-Djib.from.image=nexus.dspace.kt.co.kr/icis/icistr-sa-jre-runtime:v1.0.0 \
        			-Djib.from.auth.username=icistr-sa \
        			-Djib.from.auth.password=icistr-sa \
        			-Djib.to.image=nexus.dspace.kt.co.kr/${P_IMG_FULL_NM} \
        			-Djib.to.tags=${label} \
        			-Djib.to.auth.username=icistr-sa \
        			-Djib.to.auth.password=icistr-sa \
        			-Djib.container.jvmFlags=${JAVA_OPTS} \
					-Djib.container.environment="APP_MAIN_CLASS=${app},JAVA_OPTS_AGENT=${JAVA_OPTS}"

        			echo 'TAG ==========> ${label} '
                """			
}


def mvnBuild_ImgPush(){
			def num = ''
            if(tag == "dev" || P_BRANCH == "develop") {
                def data = new Date()
                def dataFormat = data.format("yyyyMMddHHmmss")
                num = dataFormat
                print "time tag newVersion ---${num}---"
				label = num
            }
			print "newVersion ${label}"
    return """
		set +x
	    cd ${P_PRJ_NM}
        mvn clean package jib:build -DskipTests --settings ${G_MVN_SETTINGS_PATH}/settings_${P_DOMAIN}.xml \
			-Djib.from.image=nexus.dspace.kt.co.kr/icis/icistr-sa-jre-runtime:v1.0.0 \
			-Djib.from.auth.username=icistr-sa \
			-Djib.from.auth.password=icistr-sa \
			-Djib.to.image=nexus.dspace.kt.co.kr/${P_IMG_FULL_NM} \
			-Djib.to.tags=${P_TAG} \
			-Djib.to.auth.username=icistr-sa \
			-Djib.to.auth.password=icistr-sa \
			-Djib.container.jvmFlags=-Duser.language=ko,-Duser.country=KR
					
			echo 'TAG ==========> '${P_TAG} """
}

def mvnBuild_ImgPush(tag){

            def num = ''
            if(tag == "dev" || P_BRANCH == "develop") {
                def data = new Date()
                def dataFormat = data.format("yyyyMMddHHmmss")
                num = dataFormat
                print "time tag newVersion ---${num}---"
                label = num
            }	
                print "newVersion ${label}"
                return """
                set +x
        	    cd ${P_PRJ_NM}
                mvn clean package jib:build -DskipTests --settings ${G_MVN_SETTINGS_PATH}/settings_${P_DOMAIN}.xml \
        			-Djib.from.image=nexus.dspace.kt.co.kr/icis/icistr-sa-jre-runtime:v1.0.0 \
        			-Djib.from.auth.username=icistr-sa \
        			-Djib.from.auth.password=icistr-sa \
        			-Djib.to.image=nexus.dspace.kt.co.kr/${P_IMG_FULL_NM} \
        			-Djib.to.tags=${label} \
        			-Djib.to.auth.username=icistr-sa \
        			-Djib.to.auth.password=icistr-sa \
        			-Djib.container.jvmFlags=-Duser.language=ko,-Duser.country=KR \
        
        			echo 'TAG ==========> ${label} '
                """
}

def podman_build(tag1){
	print "label --${label}--"
	return """
		set +x

		ls -al /etc/containers
		cd ${P_PRJ_NM}
		sed 's/dev/rel/g' Dockerfile-sit
		cat Dockerfile-sit
		podman login -u icistr-sa -p icistr-sa nexus.dspace.kt.co.kr --tls-verify=false
		podman build -t nexus.dspace.kt.co.kr/icis/${P_PRJ_NM}:${label} --cgroup-manager=cgroupfs --tls-verify=false -f ./Dockerfile-sit .
		podman push nexus.dspace.kt.co.kr/icis/${P_PRJ_NM}:${label} --tls-verify=false

		echo 'TAG ==========> ' """ +label

	print "newVersion ---${label}---"
}

def devTag(){
	def data = new Date()
	def dataFormat = data.format("yyyyMMddHHmmss")
	label = dataFormat
	return "echo 'TAG ==========> '" +label

}


```

