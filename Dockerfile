FROM continuumio/miniconda3:latest

# Create and activate test environment
RUN conda create -n test python=3.8
RUN echo "source activate test" > ~/.bashrc
ENV PATH /opt/conda/envs/test/bin:$PATH
RUN /bin/bash -c "source activate test"

# Copy directory into the container
COPY . /root/chatgpt-wecom

RUN cd /root/chatgpt-wecom && \
    pip install -r requirements.txt

# Set working directory and execute the script
WORKDIR /root/chatgpt-wecom
CMD ["python", "src/bot.py"]
