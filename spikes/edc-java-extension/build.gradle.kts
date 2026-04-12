import org.gradle.api.tasks.compile.JavaCompile
import org.gradle.jvm.toolchain.JavaLanguageVersion

plugins {
    `java-library`
}

group = "org.agentevidence.spike"
version = "0.0.1-SPIKE"

val javaVersion = providers.gradleProperty("javaVersion").orElse("17").get().toInt()
val edcGroup = providers.gradleProperty("edcGroup").orElse("org.eclipse.edc").get()
val edcVersion = providers.gradleProperty("edcVersion").orElse("0.17.0-SNAPSHOT").get()

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(javaVersion))
    }
    withSourcesJar()
}

repositories {
    mavenCentral()
    maven {
        url = uri("https://central.sonatype.com/repository/maven-snapshots/")
    }
}

dependencies {
    compileOnly("$edcGroup:boot-spi:$edcVersion")
    compileOnly("$edcGroup:core-spi:$edcVersion")
    compileOnly("$edcGroup:transaction-spi:$edcVersion")
    compileOnly("$edcGroup:runtime-metamodel:$edcVersion")
    compileOnly("$edcGroup:asset-spi:$edcVersion")
    compileOnly("$edcGroup:policy-spi:$edcVersion")
    compileOnly("$edcGroup:contract-spi:$edcVersion")
    compileOnly("$edcGroup:transfer-spi:$edcVersion")

    testImplementation(platform("org.junit:junit-bom:5.10.2"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testImplementation("$edcGroup:core-spi:$edcVersion")
    testImplementation("$edcGroup:transaction-spi:$edcVersion")
    testImplementation("$edcGroup:asset-spi:$edcVersion")
    testImplementation("$edcGroup:policy-spi:$edcVersion")
    testImplementation("$edcGroup:contract-spi:$edcVersion")
    testImplementation("$edcGroup:transfer-spi:$edcVersion")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.withType<JavaCompile>().configureEach {
    options.release.set(javaVersion)
}

tasks.test {
    useJUnitPlatform()
}

tasks.register("printSpikeAssumptions") {
    doLast {
        println("Java extension skeleton spike")
        println("javaVersion=$javaVersion")
        println("edcGroup=$edcGroup")
        println("edcVersion=$edcVersion")
        println("This build models an extension module, not a full connector runtime.")
    }
}
