FROM instrumentisto/cargo-ndk
RUN apt-get update -y && \
    apt-get install -y pkg-config libssl-dev

WORKDIR /app

# Copy the project files into the container
COPY . /app

# Add additional Rust targets
RUN rustup target add \
    aarch64-linux-android \
    armv7-linux-androideabi \
    x86_64-linux-android \
    i686-linux-android

# Set default values for environment variables
ENV CARGO_NDK_ANDROID_PLATFORM=21
ENV CARGO_NDK_ANDROID_TARGET=armeabi-v7a
ENV CARGO_NDK_OUTPUT_PATH=./output
ENV CARGO_NDK_SYSROOT_PATH=/usr/local/android-ndk/sysroot
ENV CARGO_NDK_SYSROOT_TARGET=arm-linux-androideabi
ENV CARGO_NDK_SYSROOT_LIBS_PATH=$CARGO_NDK_SYSROOT_PATH/usr/lib/$CARGO_NDK_SYSROOT_TARGET

# Run the cargo-ndk command
CMD ["cargo", "ndk", "-o", "./jniLibs", "build"]

#docker run --rm -v C:\Users\UCHE\Desktop\docker:/app bukki