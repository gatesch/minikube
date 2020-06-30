def gitCommit() {
        sh "git rev-parse HEAD > GIT_COMMIT"
        def gitCommit = readFile('GIT_COMMIT').trim()
        sh "rm -f GIT_COMMIT"
        return gitCommit
    }

def answerQuestion = ''

    node {
        // Checkout source code from Git
        stage 'Checkout'
        checkout scm

        // PHPUnit test
        stage 'Unit Test'
        sh "phpunit --bootstrap src/Email.php tests"

//        stage 'SCA / Nexus'
//        sh "/opt/Fortify/Fortify_SCA_and_Apps_19.1.0/bin/sourceanalyzer -b openshift-mf -clean"
 //       sh "/opt/Fortify/Fortify_SCA_and_Apps_19.1.0/bin/sourceanalyzer -b openshift-mf *.php"
  //      sh "/opt/Fortify/Fortify_SCA_and_Apps_19.1.0/bin/sourceanalyzer -b openshift-mf -scan -mt -f openshift-mf.fpr"
   //     sh "/opt/Fortify/Fortify_SCA_and_Apps_19.1.0/bin/ReportGenerator -format xml -source openshift-mf.fpr -f test.xml"
    //    sh "/opt/Fortify/Fortify_SCA_and_Apps_19.1.0/bin/ReportGenerator -format rtf -source openshift-mf.fpr -f test.rtf"

     //   sh "curl -v -u admin:redhat12 --upload-file test.rtf http://nexus.example.loc/repository/reports/report`date +%F-%T`.rtf"


        // Build Docker image
        stage 'Build'
        sh "docker build -t quay.io/gatesch/php:${gitCommit()} ."

        // Login to DTR 
        stage 'Login'
        withCredentials(
            [[
                $class: 'UsernamePasswordMultiBinding',
                credentialsId: 'dtr',
                passwordVariable: 'DTR_PASSWORD',
                usernameVariable: 'DTR_USERNAME'
            ]]
        ){ 
        sh "docker login -u gatesch -p ${env.DTR_PASSWORD}  quay.io"}

        // Push the image 
        stage 'Push'
        sh "docker push quay.io/gatesch/php:${gitCommit()}"

//        clean all
          stage('Deploy test') 

          script {
          answerQ = sh (returnStdout: true, script: "kubectl get ns |grep php |awk '{print \$1}'")
          }

          if ( answerQ != "" ) {
                sh "kubectl set image deployment php-safe -n php php=quay.io/gatesch/php:${gitCommit()}"
           }

           else {
                sh "kubectl create ns php"
        	sh "kubectl create -f limits.yaml"
        	sh "kubectl create deployment php-safe -n php --image=quay.io/gatesch/php:${gitCommit()}"
        	sh "kubectl expose deployment php-safe --port=80 --name=php-service -n php"
        	sh "kubectl create -f php-ingress.yaml"
           }

        // functional test
        stage 'Selenium'
        sh "./selenium-test.py"
    }

        stage('Deploy approval'){
             input "Deploy to prod?"
        }
	
	node {
        stage('Deploy prod')

              script {
                     answerP = sh (returnStdout: true, script: "kubectl get ns |grep php-prod |awk '{print \$1}'")
          }

          if ( answerP != "" ) {
                sh "kubectl set image deployment php-safe -n php-prod php=quay.io/gatesch/php:${gitCommit()}"
           }

           else {
                sh "kubectl create ns php-prod"
                sh "kubectl create -f limits-prod.yaml"
                sh "kubectl create deployment php-safe -n php-prod --image=quay.io/gatesch/php:${gitCommit()}"
                sh "kubectl expose deployment php-safe --port=80 --name=php-service -n php-prod"
                sh "kubectl create -f php-prod-ingress.yaml"
                sh "kubectl autoscale deployment php-safe --cpu-percent=50 --min=1 --max=10 -n php-prod"
           }
	}

