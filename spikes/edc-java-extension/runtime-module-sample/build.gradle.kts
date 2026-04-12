import org.gradle.jvm.toolchain.JavaLanguageVersion

plugins {
    `java-library`
    id("application")
}

val javaVersion = providers.gradleProperty("javaVersion").orElse("17").get().toInt()
val edcGroup = providers.gradleProperty("edcGroup").orElse("org.eclipse.edc").get()
val edcVersion = providers.gradleProperty("edcVersion").orElse("0.17.0-SNAPSHOT").get()

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(javaVersion))
    }
}

repositories {
    mavenCentral()
    maven {
        url = uri("https://central.sonatype.com/repository/maven-snapshots/")
    }
}

dependencies {
    implementation("$edcGroup:boot:$edcVersion")
    implementation("$edcGroup:runtime-core:$edcVersion")
    implementation("$edcGroup:connector-core:$edcVersion")
    implementation("$edcGroup:configuration-filesystem:$edcVersion")
    implementation("$edcGroup:http:$edcVersion")

    runtimeOnly(project(":"))
    runtimeOnly("$edcGroup:asset-spi:$edcVersion")
    runtimeOnly("$edcGroup:policy-spi:$edcVersion")
    runtimeOnly("$edcGroup:contract-spi:$edcVersion")
    runtimeOnly("$edcGroup:transfer-spi:$edcVersion")
    runtimeOnly("$edcGroup:transaction-spi:$edcVersion")

    testImplementation(platform("org.junit:junit-bom:5.10.2"))
    testImplementation("org.junit.jupiter:junit-jupiter")
    testImplementation("$edcGroup:boot-spi:$edcVersion")
    testImplementation("$edcGroup:core-spi:$edcVersion")
    testImplementation("$edcGroup:transaction-spi:$edcVersion")
    testImplementation("$edcGroup:asset-spi:$edcVersion")
    testImplementation("$edcGroup:policy-spi:$edcVersion")
    testImplementation("$edcGroup:contract-spi:$edcVersion")
    testImplementation("$edcGroup:transfer-spi:$edcVersion")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

application {
    mainClass.set("org.eclipse.edc.boot.system.runtime.BaseRuntime")
}

tasks.test {
    useJUnitPlatform()
    dependsOn(tasks.installDist)
}
